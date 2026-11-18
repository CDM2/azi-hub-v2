-- REV-01 fix pass: the permission service's database. Run as a superuser:
--   psql -v ON_ERROR_STOP=1 -v owner_pw=... -v app_pw=... -f schema.sql
--
-- What changed from spikes/r-02/service/schema.sql, and why, is in ../CONTRACT.md and ../README.md.
-- In short: the service's database login (brain_app) can no longer touch any table. It can only call
-- the functions granted at the bottom of this file. Each of those functions reads the caller's
-- organization from a session that only brain.begin_session() can bind, does one thing, and writes
-- its own row in the append-only log before it returns.
--
-- Two roles. brain_owner owns the objects and stands in for the operator's console.
-- brain_app is what agent and human calls run as.

do $$ begin
  if not exists (select 1 from pg_roles where rolname = 'brain_owner') then
    create role brain_owner login nosuperuser nocreatedb nocreaterole nobypassrls;
  end if;
  if not exists (select 1 from pg_roles where rolname = 'brain_app') then
    create role brain_app login nosuperuser nocreatedb nocreaterole nobypassrls;
  end if;
end $$;
alter role brain_owner password :'owner_pw';
alter role brain_app password :'app_pw';

drop schema if exists brain cascade;
create schema brain authorization brain_owner;
set role brain_owner;

-- Tables ------------------------------------------------------------------------------------------

-- Deployment-wide switches. personal_enabled and briefing_enabled are master switches; each person
-- also has their own (brain.people). holding_reads is the default for what a parent reads of a child.
create table brain.settings (
  id boolean primary key default true check (id),
  personal_enabled boolean not null default true,
  briefing_enabled boolean not null default true,
  holding_reads text not null default 'all' check (holding_reads in ('all', 'summaries'))
);

-- The tier map. A sub-organization has a parent; a holding organization and a personal space do not.
-- parent_reads is this organization's own answer to "what may my parent read of me": null means the default.
create table brain.orgs (
  id text primary key,
  kind text not null check (kind in ('personal', 'holding', 'sub')),
  parent_id text references brain.orgs (id),
  parent_reads text check (parent_reads in ('all', 'summaries', 'none')),
  unique (id, kind),
  check ((kind = 'sub') = (parent_id is not null)),
  check (parent_reads is null or kind = 'sub')
);

-- A person. A person may have a personal space, and it has its own two switches.
create table brain.people (
  id text primary key check (char_length(id) between 1 and 60),
  personal_org text unique,
  personal_kind text not null default 'personal' check (personal_kind = 'personal'),
  personal_enabled boolean not null default true,
  push_enabled boolean not null default true,
  foreign key (personal_org, personal_kind) references brain.orgs (id, kind) on delete cascade
);

-- Who belongs to which organization. Nobody is a member of a personal space.
create table brain.memberships (
  person_id text not null references brain.people (id) on delete cascade,
  org_id text not null,
  org_kind text not null check (org_kind in ('holding', 'sub')),
  role text not null check (role in ('owner', 'member')),
  primary key (person_id, org_id),
  foreign key (org_id, org_kind) references brain.orgs (id, kind) on delete cascade
);
create index memberships_org on brain.memberships (org_id);

-- A token acts for one organization. It may also stand for a person (always, in a personal space).
create table brain.principals (
  token_sha256 text primary key,
  org_id text not null references brain.orgs (id) on delete cascade,
  actor text not null check (actor in ('agent', 'human')),
  person_id text references brain.people (id) on delete cascade
);

-- Which organization the current transaction acts for, and what it may read. Written only by begin_session().
create unlogged table brain.sessions (
  pid int primary key,
  txid bigint not null,
  org_id text not null,
  kind text not null,
  actor text not null,
  person_id text,
  all_orgs text[] not null,      -- organizations read in full
  sum_orgs text[] not null,      -- organizations of which only summaries are read
  glob_orgs text[] not null,     -- organizations of which only approved global pages are read
  briefings_on boolean not null, -- the master briefing switch
  muted_orgs text[] not null     -- personal spaces whose own briefing switch is off
);

create table brain.pages (
  id uuid not null default gen_random_uuid(),
  org_id text not null,
  org_kind text not null,
  title text not null check (char_length(title) between 1 and 300),
  body text not null default '' check (char_length(body) <= 200000),
  kind text not null default 'note' check (kind in ('note', 'summary', 'briefing', 'report', 'code_file', 'code_package', 'code_overview')),
  source_type text not null default 'agent' check (source_type in ('human', 'agent', 'codebase')),
  sensitivity text not null default 'normal' check (sensitivity in ('normal', 'health', 'finance')),
  visibility text not null default 'org' check (visibility in ('org', 'global')),
  global_approved_by text,       -- the person who approved a global page; until then only its own organization reads it
  global_approved_at timestamptz,
  pushed_from text,              -- the organization an approved push came from
  written_by text,               -- the person behind the token that wrote the page, when there is one
  path text,
  content_sha text,
  meta jsonb not null default '{}',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  -- The organization comes first in the key on purpose: a lookup starts from the organizations the
  -- caller may read and never visits another organization's row. See brain.t_get.
  primary key (org_id, id),
  foreign key (org_id, org_kind) references brain.orgs (id, kind) on delete cascade,
  constraint health_and_finance_stay_personal check (sensitivity = 'normal' or org_kind = 'personal'),
  constraint only_holding_publishes_global check (visibility = 'org' or org_kind = 'holding'),
  constraint approval_is_for_global_pages check ((global_approved_at is null and global_approved_by is null)
                                                 or (visibility = 'global' and global_approved_at is not null and global_approved_by is not null)),
  constraint pushed_pages_name_their_source check ((kind in ('briefing', 'report')) = (pushed_from is not null))
);
create unique index pages_org_path on brain.pages (org_id, path) where path is not null;
-- The few global pages that wait for a person: found without walking every organization's pages.
create index pages_pending_global on brain.pages (org_id) where visibility = 'global' and global_approved_at is null;

-- A push: text one organization offers to another. Nobody at the receiving end reads it until a
-- person with authority over the source approves it. Two kinds exist: a personal space to an
-- organization its person belongs to (a briefing), and a sub-organization to its parent (a report).
create table brain.pushes (
  id uuid primary key default gen_random_uuid(),
  from_org text not null references brain.orgs (id) on delete cascade,
  to_org text not null references brain.orgs (id) on delete cascade,
  content text not null check (char_length(content) between 1 and 2000),
  status text not null default 'pending' check (status in ('pending', 'approved', 'rejected')),
  created_at timestamptz not null default now(),
  created_by_actor text not null,
  created_by_person text,
  decided_by text,
  decided_at timestamptz,
  decided_via text check (decided_via in ('human_token', 'operator')),
  page_id uuid,
  check (from_org <> to_org),
  check ((status = 'pending') = (decided_at is null)),
  check ((status = 'pending') = (decided_by is null)),
  check ((status = 'approved') = (page_id is not null))
);
create function brain.pushes_are_decided_once() returns trigger language plpgsql as $$
begin
  if tg_op = 'DELETE' then raise exception 'a push is never deleted'; end if;
  if old.status <> 'pending' then raise exception 'a push is decided once'; end if;
  if (new.id, new.from_org, new.to_org, new.content, new.created_at, new.created_by_actor, new.created_by_person)
     is distinct from (old.id, old.from_org, old.to_org, old.content, old.created_at, old.created_by_actor, old.created_by_person) then
    raise exception 'the text and the route of a push cannot change after it is written';
  end if;
  return new;
end $$;
create trigger pushes_no_rewrite before update or delete on brain.pushes
  for each row execute function brain.pushes_are_decided_once();

-- The log. One row for every call, allowed or denied, by an agent, a person or the operator.
-- Append-only: triggers refuse change, and each row carries a hash of the row before it, so a row
-- that is altered or removed by someone who can switch the triggers off is still detected (audit_verify).
create sequence brain.audit_id;
create table brain.audit (
  id bigint primary key,
  ts timestamptz not null,
  via text not null check (via in ('mcp', 'admin')),
  org text,
  actor text,
  person text,
  tool text not null,
  request_id text,
  decision text not null check (decision in ('allow', 'deny')),
  reason text,
  args_sha256 text,
  target text,          -- what the call named: a page id, a path, a push id
  result_count int,
  page_ids uuid[],      -- the pages the call returned or created; never their text
  detail jsonb,         -- operator actions only: what was changed
  prev_hash text,
  row_hash text not null
);
create function brain.audit_is_append_only() returns trigger language plpgsql as
$$ begin raise exception 'the audit log is append-only'; end $$;
create trigger audit_no_change before update or delete on brain.audit
  for each row execute function brain.audit_is_append_only();
create trigger audit_no_truncate before truncate on brain.audit
  for each statement execute function brain.audit_is_append_only();

create function brain.audit_hash_(p_prev text, p_id bigint, p_ts timestamptz, p_via text, p_org text, p_actor text, p_person text, p_tool text,
                                  p_request_id text, p_decision text, p_reason text, p_args_sha text, p_target text, p_count int,
                                  p_page_ids uuid[], p_detail jsonb) returns text
language sql immutable as $$
  select encode(sha256(convert_to(jsonb_build_array(p_prev, p_id, to_char(p_ts at time zone 'UTC', 'YYYY-MM-DD"T"HH24:MI:SS.US'), p_via, p_org, p_actor,
    p_person, p_tool, p_request_id, p_decision, p_reason, p_args_sha, p_target, p_count, p_page_ids::text, p_detail)::text, 'UTF8')), 'hex')
$$;

-- The only place a row enters the log. Not callable by brain_app.
create function brain.audit_write_(p_via text, p_org text, p_actor text, p_person text, p_tool text, p_request_id text, p_decision text,
                                   p_reason text, p_args_sha text, p_target text, p_count int, p_page_ids uuid[], p_detail jsonb) returns bigint
language plpgsql set search_path = brain, pg_temp as $$
declare
  v_prev text; v_id bigint; v_ts timestamptz;
  v_tool text := left(regexp_replace(coalesce(p_tool, ''), '[[:cntrl:]]', '?', 'g'), 60);
  v_rid text := left(regexp_replace(p_request_id, '[[:cntrl:]]', '?', 'g'), 100);
  v_reason text := left(regexp_replace(p_reason, '[[:cntrl:]]', '?', 'g'), 100);
  v_sha text := left(p_args_sha, 64);
  v_target text := left(regexp_replace(p_target, '[[:cntrl:]]', '?', 'g'), 200);
begin
  perform pg_advisory_xact_lock(820117);                 -- one writer at a time, so the chain has one order
  select a.row_hash into v_prev from brain.audit a order by a.id desc limit 1;
  v_id := nextval('brain.audit_id');
  v_ts := clock_timestamp();
  insert into brain.audit (id, ts, via, org, actor, person, tool, request_id, decision, reason, args_sha256, target, result_count, page_ids, detail, prev_hash, row_hash)
  values (v_id, v_ts, p_via, p_org, p_actor, p_person, v_tool, v_rid, p_decision, v_reason, v_sha, v_target, p_count, p_page_ids, p_detail, v_prev,
          brain.audit_hash_(v_prev, v_id, v_ts, p_via, p_org, p_actor, p_person, v_tool, v_rid, p_decision, v_reason, v_sha, v_target, p_count, p_page_ids, p_detail));
  return v_id;
end $$;

-- Walks the chain. Returns the first row that does not match, or null when every row matches.
create function brain.audit_verify() returns table (rows_checked bigint, first_bad_id bigint)
language plpgsql stable set search_path = brain, pg_temp as $$
declare r brain.audit; v_prev text := null; v_n bigint := 0;
begin
  for r in select * from brain.audit order by id loop
    v_n := v_n + 1;
    if r.prev_hash is distinct from v_prev
       or r.row_hash <> brain.audit_hash_(r.prev_hash, r.id, r.ts, r.via, r.org, r.actor, r.person, r.tool, r.request_id, r.decision, r.reason,
                                          r.args_sha256, r.target, r.result_count, r.page_ids, r.detail) then
      return query select v_n, r.id; return;
    end if;
    v_prev := r.row_hash;
  end loop;
  return query select v_n, null::bigint;
end $$;

-- Who belongs where ---------------------------------------------------------------------------------

-- Walk up from the organization. The first organization that has a member list decides.
-- brain.belongs_: the person is on that list (any role on the organization itself, owner on one above it).
-- brain.controls_: the person is an owner on that list.
create function brain.standing_(p_person text, p_org text, p_need_owner boolean) returns boolean
language plpgsql stable set search_path = brain, pg_temp as $$
declare v_org text := p_org; v_first boolean := true; v_role text; v_parent text;
begin
  if p_person is null or p_org is null then return false; end if;
  loop
    if exists (select 1 from brain.memberships m where m.org_id = v_org) then
      select m.role into v_role from brain.memberships m where m.org_id = v_org and m.person_id = p_person;
      return found and (v_role = 'owner' or (v_first and not p_need_owner));
    end if;
    select o.parent_id into v_parent from brain.orgs o where o.id = v_org;
    if v_parent is null then return false; end if;
    v_org := v_parent; v_first := false;
  end loop;
end $$;
create function brain.belongs_(p_person text, p_org text) returns boolean language sql stable as $$ select brain.standing_(p_person, p_org, false) $$;
create function brain.controls_(p_person text, p_org text) returns boolean language sql stable as $$ select brain.standing_(p_person, p_org, true) $$;

-- What a parent reads of one child: the child's own setting, or the default. The default is nothing
-- when the child has a member who does not control the parent (a second person), else the deployment's setting.
create function brain.child_mode_(p_child text) returns text
language sql stable set search_path = brain, pg_temp as $$
  select coalesce(c.parent_reads,
                  case when exists (select 1 from brain.memberships m where m.org_id = c.id and not brain.controls_(m.person_id, c.parent_id))
                       then 'none' else (select s.holding_reads from brain.settings s) end)
    from brain.orgs c where c.id = p_child
$$;

create function brain.root_of_(p_org text) returns text
language sql stable set search_path = brain, pg_temp as $$
  with recursive up (id, parent_id) as (
    select o.id, o.parent_id from brain.orgs o where o.id = p_org
    union all
    select o.id, o.parent_id from brain.orgs o join up on o.id = up.parent_id)
  select id from up where parent_id is null
$$;

-- Session binding -------------------------------------------------------------------------------------

-- Presents a token. Binds this transaction to the token's organization and works out, once and always,
-- which organizations it may read. Every statement here runs for every call, whatever the call goes on to ask for.
create function brain.begin_session(p_token text) returns table (org text, kind text, actor text)
language plpgsql security definer set search_path = brain, pg_temp as $$
declare
  v record; st brain.settings; v_person text;
  v_all text[]; v_sum text[] := '{}'; v_glob text[] := '{}'; v_muted text[];
begin
  select pr.org_id, o.kind, pr.actor, pr.person_id into v
    from brain.principals pr join brain.orgs o on o.id = pr.org_id
   where pr.token_sha256 = encode(sha256(convert_to(coalesce(p_token, ''), 'UTF8')), 'hex');
  if not found then raise exception 'invalid_token' using errcode = '28000'; end if;
  select * into st from brain.settings;
  v_person := v.person_id;
  v_all := array[v.org_id];

  if v.kind = 'personal' then
    -- A personal space belongs to exactly one person, and works only while both switches are on.
    select p.id into v_person from brain.people p
     where p.personal_org = v.org_id and p.personal_enabled and st.personal_enabled and (v.person_id is null or v.person_id = p.id);
    if not found then raise exception 'invalid_token' using errcode = '28000'; end if;
    -- The person reads every organization they belong to, and the approved global pages of the organization at the top of each.
    select v_all || coalesce(array_agg(o.id order by o.id), '{}') into v_all
      from brain.orgs o where o.kind <> 'personal' and brain.belongs_(v_person, o.id);
    select coalesce(array_agg(distinct r.root), '{}') into v_glob
      from (select brain.root_of_(x) as root from unnest(v_all[2:]) x) r where r.root <> all (v_all);
  else
    -- A token that stands for a person works only while that person belongs to the organization.
    if v.person_id is not null and not brain.belongs_(v.person_id, v.org_id) then
      raise exception 'invalid_token' using errcode = '28000';
    end if;
    -- An organization reads its direct children as each child allows, and the approved global pages of the organization at its top.
    select v_all || coalesce(array_agg(c.id order by c.id) filter (where brain.child_mode_(c.id) = 'all'), '{}'),
           coalesce(array_agg(c.id order by c.id) filter (where brain.child_mode_(c.id) = 'summaries'), '{}')
      into v_all, v_sum
      from brain.orgs c where c.parent_id = v.org_id;
    if v.kind = 'sub' then v_glob := array[brain.root_of_(v.org_id)]; end if;
  end if;
  select coalesce(array_agg(p.personal_org), '{}') into v_muted from brain.people p where p.personal_org is not null and not p.push_enabled;

  insert into brain.sessions (pid, txid, org_id, kind, actor, person_id, all_orgs, sum_orgs, glob_orgs, briefings_on, muted_orgs)
  values (pg_backend_pid(), txid_current(), v.org_id, v.kind, v.actor, v_person, v_all, v_sum, v_glob, st.briefing_enabled, v_muted)
  on conflict (pid) do update set txid = excluded.txid, org_id = excluded.org_id, kind = excluded.kind, actor = excluded.actor,
    person_id = excluded.person_id, all_orgs = excluded.all_orgs, sum_orgs = excluded.sum_orgs, glob_orgs = excluded.glob_orgs,
    briefings_on = excluded.briefings_on, muted_orgs = excluded.muted_orgs;
  return query select v.org_id::text, v.kind::text, v.actor::text;
end $$;

-- The bound session of this transaction, or an error. Every tool function starts here.
create function brain.scope_() returns brain.sessions
language plpgsql stable set search_path = brain, pg_temp as $$
declare s brain.sessions;
begin
  select * into s from brain.sessions where pid = pg_backend_pid() and txid = txid_current_if_assigned();
  if not found then raise exception 'no_session' using errcode = '28000'; end if;
  return s;
end $$;

-- The read rule, in one place -------------------------------------------------------------------------
-- Every read below selects from this function and from nothing else. It is plain SQL with no settings
-- of its own so that the planner folds it into the calling query.
create function brain.visible_pages_(s brain.sessions) returns setof brain.pages
language sql stable as $$
  select p.* from brain.pages p
   where (p.org_id = any ((s).all_orgs)                                                                   -- read in full
          or (p.org_id = any ((s).sum_orgs) and p.kind = 'summary')                                       -- summaries only
          or (p.org_id = any ((s).glob_orgs) and p.visibility = 'global' and p.global_approved_at is not null))  -- approved global pages
     and (p.org_kind <> 'personal' or p.org_id = (s).org_id)                                              -- second lock: nobody else reads a personal space
     and (p.kind <> 'briefing' or ((s).briefings_on and p.pushed_from <> all ((s).muted_orgs)))           -- a briefing switch that is off hides earlier briefings
$$;

create function brain.audit_allow_(s brain.sessions, p_tool text, p_request_id text, p_args_sha text, p_target text, p_count int, p_page_ids uuid[]) returns void
language sql set search_path = brain, pg_temp as $$
  select brain.audit_write_('mcp', (s).org_id, (s).actor, (s).person_id, p_tool, p_request_id, 'allow', null, p_args_sha, p_target, p_count, p_page_ids, null)
$$;

-- Tools: what brain_app may call ------------------------------------------------------------------------
-- Errors: BR400 invalid_arguments, BR403 forbidden, BR404 not_found, BR409 disabled. An error rolls the
-- transaction back; the service then records the refusal with brain.audit_denied in a new transaction.

create function brain.t_whoami(p_request_id text, p_args_sha text) returns jsonb
language plpgsql security definer set search_path = brain, pg_temp as $$
declare s brain.sessions := brain.scope_();
begin
  perform brain.audit_allow_(s, 'brain_whoami', p_request_id, p_args_sha, null, null, null);
  return jsonb_build_object('org', s.org_id, 'kind', s.kind, 'actor', s.actor, 'person', s.person_id);
end $$;

-- The two functions below carry two protections that R-02 got for free from row-level security. Each has a test that
-- fails without it (tests/test_fix_new_rules.py, class OtherOrganizationsPagesCostNothing) and a mutant in the sweep.
--
-- "set enable_seqscan = off" makes a list or a search walk the index from the caller's organizations, so that it does
-- not visit another organization's rows. Without it PostgreSQL scans the whole table whenever it runs these statements
-- from a plan it made without looking at the caller's organizations, which it does after a connection's first few calls.
--
-- "offset 0" is a fence. It makes the database apply the read rule first and look at a row's kind, title, body or path
-- only afterwards. Without it the planner is free to try the search text against another organization's rows before it
-- discards them, and how long that takes would depend on what they say.
create function brain.t_list(p_request_id text, p_args_sha text, p_source_type text, p_kind text, p_limit int) returns jsonb
language plpgsql security definer set search_path = brain, pg_temp set enable_seqscan = off as $$
declare s brain.sessions := brain.scope_(); v_limit int := greatest(1, least(200, coalesce(p_limit, 50))); v_count int; v_pages jsonb; v_ids uuid[];
begin
  select count(*) into v_count from (select * from brain.visible_pages_(s) offset 0) p
   where (p_source_type is null or p.source_type = p_source_type) and (p_kind is null or p.kind = p_kind);
  select coalesce(jsonb_agg(jsonb_build_object('id', x.id, 'org', x.org_id, 'title', x.title, 'kind', x.kind, 'source_type', x.source_type, 'path', x.path)
                            order by x.org_id, x.sort_key, x.id), '[]'), coalesce(array_agg(x.id), '{}')
    into v_pages, v_ids
    from (select p.id, p.org_id, p.title, p.kind, p.source_type, p.path, coalesce(p.path, p.title) as sort_key from (select * from brain.visible_pages_(s) offset 0) p
           where (p_source_type is null or p.source_type = p_source_type) and (p_kind is null or p.kind = p_kind)
           order by p.org_id, coalesce(p.path, p.title), p.id limit v_limit) x;
  perform brain.audit_allow_(s, 'brain_list', p_request_id, p_args_sha, null, v_count, v_ids);
  return jsonb_build_object('count', v_count, 'pages', v_pages);
end $$;

create function brain.t_search(p_request_id text, p_args_sha text, p_query text, p_source_type text, p_limit int) returns jsonb
language plpgsql security definer set search_path = brain, pg_temp set enable_seqscan = off as $$
declare
  s brain.sessions := brain.scope_(); v_limit int := greatest(1, least(200, coalesce(p_limit, 50))); v_count int; v_pages jsonb; v_ids uuid[];
  v_like text;
begin
  if p_query is null or btrim(p_query) = '' or char_length(p_query) > 10000 then raise exception 'invalid_arguments' using errcode = 'BR400'; end if;
  v_like := '%' || replace(replace(replace(left(p_query, 500), '\', '\\'), '%', '\%'), '_', '\_') || '%';
  select count(*) into v_count from (select * from brain.visible_pages_(s) offset 0) p
   where (p.title ilike v_like escape '\' or p.body ilike v_like escape '\' or p.path ilike v_like escape '\')
     and (p_source_type is null or p.source_type = p_source_type);
  select coalesce(jsonb_agg(jsonb_build_object('id', x.id, 'org', x.org_id, 'title', x.title, 'kind', x.kind, 'source_type', x.source_type, 'path', x.path,
                                               'snippet', x.snippet) order by x.org_id, x.sort_key, x.id), '[]'), coalesce(array_agg(x.id), '{}')
    into v_pages, v_ids
    from (select p.id, p.org_id, p.title, p.kind, p.source_type, p.path, left(p.body, 300) as snippet, coalesce(p.path, p.title) as sort_key
            from (select * from brain.visible_pages_(s) offset 0) p
           where (p.title ilike v_like escape '\' or p.body ilike v_like escape '\' or p.path ilike v_like escape '\')
             and (p_source_type is null or p.source_type = p_source_type)
           order by p.org_id, coalesce(p.path, p.title), p.id limit v_limit) x;
  perform brain.audit_allow_(s, 'brain_search', p_request_id, p_args_sha, null, v_count, v_ids);
  return jsonb_build_object('count', v_count, 'pages', v_pages);
end $$;

-- One page by id or by path. p_org narrows the lookup to one organization the caller may already read; it never widens it.
--
-- The lookup asks each readable organization in turn for (organization, id) or (organization, path), with the
-- organization written first. A row in any other organization fails on the organization and its id or path is
-- never compared, so a page the caller may not read costs exactly what a page that does not exist costs, and
-- gives the same error. (R-02's version compared first and filtered after, which is what REV-01 RV-06 measured.)
create function brain.t_get(p_request_id text, p_args_sha text, p_id uuid, p_path text, p_org text) returns jsonb
language plpgsql security definer set search_path = brain, pg_temp as $$
declare
  s brain.sessions := brain.scope_(); r brain.pages; hit brain.pages; v_org text; v_orgs text[]; v_others text[] := '{}';
  v_path text := left(p_path, 1000); v_page jsonb;
begin
  if p_id is null and p_path is null then raise exception 'invalid_arguments' using errcode = 'BR400'; end if;
  select coalesce(array_agg(distinct o order by o), '{}') into v_orgs from unnest(s.all_orgs || s.sum_orgs || s.glob_orgs) o where p_org is null or o = p_org;
  foreach v_org in array v_orgs loop
    if p_id is not null then
      select p.* into r from brain.visible_pages_(s) p where p.org_id = v_org and p.id = p_id;
    else
      select p.* into r from brain.visible_pages_(s) p where p.org_id = v_org and p.path = v_path;
    end if;
    if found then
      if hit.id is null then hit := r; else v_others := v_others || r.org_id; end if;
    end if;
  end loop;
  if hit.id is null then raise exception 'not_found' using errcode = 'BR404'; end if;
  v_page := jsonb_build_object('id', hit.id, 'org', hit.org_id, 'title', hit.title, 'body', hit.body, 'kind', hit.kind, 'source_type', hit.source_type,
                               'sensitivity', hit.sensitivity, 'visibility', hit.visibility, 'path', hit.path, 'meta', hit.meta, 'updated_at', hit.updated_at,
                               'written_by', hit.written_by, 'pushed_from', hit.pushed_from);
  if hit.visibility = 'global' and hit.global_approved_at is null then v_page := v_page || jsonb_build_object('status', 'pending_approval'); end if;
  perform brain.audit_allow_(s, 'brain_get', p_request_id, p_args_sha, coalesce(p_id::text, p_path), 1, array[hit.id]);
  return jsonb_build_object('page', v_page) || case when cardinality(v_others) > 0 then jsonb_build_object('other_orgs', to_jsonb(v_others)) else '{}'::jsonb end;
end $$;

-- A note or a summary in the caller's own organization. A global page from an agent, or from a person who does
-- not control the organization, is stored but stays unread outside the organization until a person who does approves it.
create function brain.t_write(p_request_id text, p_args_sha text, p_title text, p_body text, p_kind text, p_sensitivity text, p_visibility text) returns jsonb
language plpgsql security definer set search_path = brain, pg_temp as $$
declare
  s brain.sessions := brain.scope_(); v_id uuid := gen_random_uuid();
  v_kind text := coalesce(p_kind, 'note'); v_vis text := coalesce(p_visibility, 'org'); v_approved boolean;
begin
  if v_kind not in ('note', 'summary') then raise exception 'forbidden' using errcode = 'BR403'; end if;
  v_approved := v_vis = 'global' and s.actor = 'human' and brain.controls_(s.person_id, s.org_id);
  insert into brain.pages (id, org_id, org_kind, title, body, kind, sensitivity, visibility, source_type, written_by, global_approved_by, global_approved_at)
  values (v_id, s.org_id, s.kind, p_title, p_body, v_kind, coalesce(p_sensitivity, 'normal'), v_vis,
          case s.actor when 'human' then 'human' else 'agent' end, s.person_id,
          case when v_approved then s.person_id end, case when v_approved then now() end);
  perform brain.audit_allow_(s, 'brain_write', p_request_id, p_args_sha, null, 1, array[v_id]);
  return jsonb_build_object('id', v_id) || case when v_vis = 'global' and not v_approved then jsonb_build_object('status', 'pending_approval') else '{}'::jsonb end;
end $$;

-- Personal space only: offer a short briefing to an organization the person belongs to.
-- With no target it goes to the one top-level organization the person owns; with more than one the target must be named.
create function brain.t_publish_briefing(p_request_id text, p_args_sha text, p_content text, p_to text) returns jsonb
language plpgsql security definer set search_path = brain, pg_temp as $$
declare s brain.sessions := brain.scope_(); v_to text := p_to; v_roots text[]; v_id uuid := gen_random_uuid();
begin
  if p_content is null or btrim(p_content) = '' or char_length(p_content) > 2000 then raise exception 'invalid_arguments' using errcode = 'BR400'; end if;
  if s.kind <> 'personal' then raise exception 'forbidden' using errcode = 'BR403'; end if;
  if not s.briefings_on or s.org_id = any (s.muted_orgs) then raise exception 'disabled' using errcode = 'BR409'; end if;
  if v_to is null then
    select array_agg(m.org_id) into v_roots from brain.memberships m join brain.orgs o on o.id = m.org_id
     where m.person_id = s.person_id and m.role = 'owner' and o.parent_id is null;
    if v_roots is null or cardinality(v_roots) <> 1 then raise exception 'invalid_arguments' using errcode = 'BR400'; end if;
    v_to := v_roots[1];
  end if;
  if v_to = s.org_id or v_to <> all (s.all_orgs) then raise exception 'forbidden' using errcode = 'BR403'; end if;
  insert into brain.pushes (id, from_org, to_org, content, created_by_actor, created_by_person) values (v_id, s.org_id, v_to, p_content, s.actor, s.person_id);
  perform brain.audit_allow_(s, 'publish_briefing', p_request_id, p_args_sha, v_id::text, null, null);
  return jsonb_build_object('briefing_id', v_id, 'status', 'pending', 'to', v_to);
end $$;

-- Sub-organization only: offer a short report to the organization above.
create function brain.t_push_to_parent(p_request_id text, p_args_sha text, p_content text) returns jsonb
language plpgsql security definer set search_path = brain, pg_temp as $$
declare s brain.sessions := brain.scope_(); v_to text; v_id uuid := gen_random_uuid();
begin
  if p_content is null or btrim(p_content) = '' or char_length(p_content) > 2000 then raise exception 'invalid_arguments' using errcode = 'BR400'; end if;
  select o.parent_id into v_to from brain.orgs o where o.id = s.org_id and o.kind = 'sub';
  if v_to is null then raise exception 'forbidden' using errcode = 'BR403'; end if;
  insert into brain.pushes (id, from_org, to_org, content, created_by_actor, created_by_person) values (v_id, s.org_id, v_to, p_content, s.actor, s.person_id);
  perform brain.audit_allow_(s, 'push_to_parent', p_request_id, p_args_sha, v_id::text, null, null);
  return jsonb_build_object('push_id', v_id, 'status', 'pending', 'to', v_to);
end $$;

-- Approval ------------------------------------------------------------------------------------------------

-- Who may decide a push: for a personal space, its own person; for an organization, a person who controls it.
create function brain.may_decide_(p_person text, p_from_org text) returns boolean
language sql stable set search_path = brain, pg_temp as $$
  select case when o.kind = 'personal' then exists (select 1 from brain.people p where p.id = p_person and p.personal_org = o.id)
              else brain.controls_(p_person, o.id) end
    from brain.orgs o where o.id = p_from_org
$$;

-- The decision itself. A push the person may not decide looks exactly like a push that does not exist.
create function brain.decide_push_(p_push uuid, p_person text, p_decision text, p_via text) returns uuid
language plpgsql set search_path = brain, pg_temp as $$
declare b brain.pushes; st brain.settings; pp brain.people; v_from_kind text; v_to_kind text; v_page uuid := gen_random_uuid(); v_kind text; v_title text;
begin
  if coalesce(p_decision, 'approve') not in ('approve', 'reject') then raise exception 'invalid_arguments' using errcode = 'BR400'; end if;
  select * into b from brain.pushes where id = p_push and status = 'pending' for update;
  if not found or not coalesce(brain.may_decide_(p_person, b.from_org), false) then raise exception 'not_found' using errcode = 'BR404'; end if;
  if p_decision = 'reject' then
    update brain.pushes set status = 'rejected', decided_by = p_person, decided_at = now(), decided_via = p_via where id = p_push;
    return null;
  end if;
  select o.kind into v_from_kind from brain.orgs o where o.id = b.from_org;
  select o.kind into v_to_kind from brain.orgs o where o.id = b.to_org;
  if v_from_kind = 'personal' then
    -- Nothing new leaves a personal space while any of its switches is off.
    select * into st from brain.settings;
    select * into pp from brain.people p where p.personal_org = b.from_org;
    if not (st.briefing_enabled and pp.push_enabled and st.personal_enabled and pp.personal_enabled) then
      raise exception 'disabled' using errcode = 'BR409';
    end if;
    v_kind := 'briefing'; v_title := 'Briefing from the personal space, ' || to_char(now(), 'YYYY-MM-DD');
  else
    v_kind := 'report'; v_title := 'Report from ' || b.from_org || ', ' || to_char(now(), 'YYYY-MM-DD');
  end if;
  insert into brain.pages (id, org_id, org_kind, title, body, kind, source_type, pushed_from, written_by)
  values (v_page, b.to_org, v_to_kind, v_title, b.content, v_kind, 'human', b.from_org, p_person);
  update brain.pushes set status = 'approved', decided_by = p_person, decided_at = now(), decided_via = p_via, page_id = v_page where id = p_push;
  return v_page;
end $$;

-- A pending global page: approved by a person who controls its organization, or sent back to being an ordinary page.
create function brain.decide_page_(p_page uuid, p_person text, p_decision text) returns uuid
language plpgsql set search_path = brain, pg_temp as $$
declare r brain.pages;
begin
  if coalesce(p_decision, 'approve') not in ('approve', 'reject') then raise exception 'invalid_arguments' using errcode = 'BR400'; end if;
  select * into r from brain.pages where id = p_page and visibility = 'global' and global_approved_at is null for update;
  if not found or not brain.controls_(p_person, r.org_id) then raise exception 'not_found' using errcode = 'BR404'; end if;
  if p_decision = 'reject' then
    update brain.pages set visibility = 'org', updated_at = now() where org_id = r.org_id and id = r.id;
  else
    update brain.pages set global_approved_by = p_person, global_approved_at = now(), updated_at = now() where org_id = r.org_id and id = r.id;
  end if;
  return r.id;
end $$;

-- For a person only, never an agent: what is waiting for this person's decision, with the text, so that nothing is approved unread.
create function brain.t_pending_approvals(p_request_id text, p_args_sha text) returns jsonb
language plpgsql security definer set search_path = brain, pg_temp as $$
declare s brain.sessions := brain.scope_(); v_pushes jsonb; v_pages jsonb; v_ids uuid[];
begin
  if s.actor <> 'human' or s.person_id is null then raise exception 'forbidden' using errcode = 'BR403'; end if;
  select coalesce(jsonb_agg(jsonb_build_object('push_id', b.id, 'from', b.from_org, 'to', b.to_org, 'content', b.content, 'created_at', b.created_at,
                                               'written_by_actor', b.created_by_actor) order by b.created_at, b.id), '[]')
    into v_pushes from brain.pushes b where b.status = 'pending' and brain.may_decide_(s.person_id, b.from_org);
  select coalesce(jsonb_agg(jsonb_build_object('page_id', p.id, 'org', p.org_id, 'title', p.title, 'body', p.body, 'source_type', p.source_type)
                            order by p.created_at, p.id), '[]'), coalesce(array_agg(p.id), '{}')
    into v_pages, v_ids from brain.pages p where p.visibility = 'global' and p.global_approved_at is null and brain.controls_(s.person_id, p.org_id);
  perform brain.audit_allow_(s, 'pending_approvals', p_request_id, p_args_sha, null, jsonb_array_length(v_pushes) + jsonb_array_length(v_pages), v_ids);
  return jsonb_build_object('pushes', v_pushes, 'pages', v_pages);
end $$;

create function brain.t_decide_push(p_request_id text, p_args_sha text, p_push uuid, p_decision text) returns jsonb
language plpgsql security definer set search_path = brain, pg_temp as $$
declare s brain.sessions := brain.scope_(); v_page uuid;
begin
  if s.actor <> 'human' or s.person_id is null then raise exception 'forbidden' using errcode = 'BR403'; end if;
  v_page := brain.decide_push_(p_push, s.person_id, p_decision, 'human_token');
  perform brain.audit_allow_(s, 'approve_push', p_request_id, p_args_sha, p_push::text, null, case when v_page is not null then array[v_page] end);
  return jsonb_build_object('push_id', p_push, 'status', case when v_page is null then 'rejected' else 'approved' end, 'page_id', v_page);
end $$;

create function brain.t_decide_page(p_request_id text, p_args_sha text, p_page uuid, p_decision text) returns jsonb
language plpgsql security definer set search_path = brain, pg_temp as $$
declare s brain.sessions := brain.scope_(); v_page uuid;
begin
  if s.actor <> 'human' or s.person_id is null then raise exception 'forbidden' using errcode = 'BR403'; end if;
  v_page := brain.decide_page_(p_page, s.person_id, p_decision);
  perform brain.audit_allow_(s, 'approve_page', p_request_id, p_args_sha, p_page::text, null, array[v_page]);
  return jsonb_build_object('page_id', v_page, 'status', case when coalesce(p_decision, 'approve') = 'reject' then 'rejected' else 'approved' end);
end $$;

-- Log rows the service writes for what the functions above cannot: refusals and non-tool messages --------------

-- A refusal. Needs a bound session, and can only ever write "deny".
create function brain.audit_denied(p_tool text, p_request_id text, p_reason text, p_args_sha text, p_target text) returns void
language plpgsql security definer set search_path = brain, pg_temp as $$
declare s brain.sessions := brain.scope_();
begin
  perform brain.audit_write_('mcp', s.org_id, s.actor, s.person_id, p_tool, p_request_id, 'deny', coalesce(p_reason, 'denied'), p_args_sha, p_target, null, null, null);
end $$;

-- A protocol message that is not a tool call. Needs a bound session. A method it does not know is logged as refused.
create function brain.audit_rpc(p_method text) returns boolean
language plpgsql security definer set search_path = brain, pg_temp as $$
declare s brain.sessions := brain.scope_(); v_known boolean;
begin
  v_known := coalesce(p_method in ('initialize', 'ping', 'tools/list') or p_method like 'notifications/%', false);
  perform brain.audit_write_('mcp', s.org_id, s.actor, s.person_id,
                             case when not v_known then 'mcp:unknown_method' when p_method like 'notifications/%' then 'mcp:notification' else 'mcp:' || p_method end,
                             null, case when v_known then 'allow' else 'deny' end, case when v_known then null else 'unknown_method' end, null, p_method, null, null, null);
  return v_known;
end $$;

-- A token that was refused. No session exists, so the row is fixed: it can say nothing else.
create function brain.audit_auth_failure() returns void
language sql security definer set search_path = brain, pg_temp as $$
  select brain.audit_write_('mcp', null, null, null, 'auth', null, 'deny', 'invalid_token', null, null, null, null, null)
$$;

-- The operator's console (brain_owner only) -------------------------------------------------------------------

create function brain.audit_operator(p_tool text, p_decision text, p_reason text, p_org text, p_person text, p_target text, p_page_ids uuid[], p_detail jsonb) returns bigint
language sql set search_path = brain, pg_temp as $$
  select brain.audit_write_('admin', p_org, 'operator', p_person, p_tool, null, p_decision, p_reason, null, p_target, null, p_page_ids, p_detail)
$$;

-- The operator records a named person's decision. The person must exist and must have the authority; an empty name is refused.
create function brain.operator_decide_push(p_push uuid, p_approver text, p_decision text) returns uuid
language plpgsql set search_path = brain, pg_temp as $$
declare v_page uuid;
begin
  if p_approver is null or not exists (select 1 from brain.people p where p.id = p_approver) then raise exception 'not_found' using errcode = 'BR404'; end if;
  v_page := brain.decide_push_(p_push, p_approver, p_decision, 'operator');
  perform brain.audit_operator('admin:approve_briefing', 'allow', null, null, p_approver, p_push::text, case when v_page is not null then array[v_page] end,
                               jsonb_build_object('decision', coalesce(p_decision, 'approve'), 'on_behalf_of', p_approver));
  return v_page;
end $$;

create function brain.operator_decide_page(p_page uuid, p_approver text, p_decision text) returns uuid
language plpgsql set search_path = brain, pg_temp as $$
declare v_page uuid;
begin
  if p_approver is null or not exists (select 1 from brain.people p where p.id = p_approver) then raise exception 'not_found' using errcode = 'BR404'; end if;
  v_page := brain.decide_page_(p_page, p_approver, p_decision);
  perform brain.audit_operator('admin:approve_page', 'allow', null, null, p_approver, p_page::text, array[v_page],
                               jsonb_build_object('decision', coalesce(p_decision, 'approve'), 'on_behalf_of', p_approver));
  return v_page;
end $$;

-- Row-level security stays on as a second lock. brain_app has no policy on any table, so a grant made
-- by mistake would still return no rows.
alter table brain.pages enable row level security;
alter table brain.pages force row level security;
create policy pages_console on brain.pages for all to brain_owner using (true) with check (true);
alter table brain.pushes enable row level security;
alter table brain.pushes force row level security;
create policy pushes_console on brain.pushes for all to brain_owner using (true) with check (true);

-- Privileges: start from nothing, then grant the functions and nothing else.
revoke all on all tables in schema brain from public, brain_app;
revoke all on all sequences in schema brain from public, brain_app;
revoke all on all functions in schema brain from public, brain_app;
grant usage on schema brain to brain_app;
grant execute on function
  brain.begin_session(text),
  brain.t_whoami(text, text),
  brain.t_list(text, text, text, text, int),
  brain.t_search(text, text, text, text, int),
  brain.t_get(text, text, uuid, text, text),
  brain.t_write(text, text, text, text, text, text, text),
  brain.t_publish_briefing(text, text, text, text),
  brain.t_push_to_parent(text, text, text),
  brain.t_pending_approvals(text, text),
  brain.t_decide_push(text, text, uuid, text),
  brain.t_decide_page(text, text, uuid, text),
  brain.audit_denied(text, text, text, text, text),
  brain.audit_rpc(text),
  brain.audit_auth_failure()
to brain_app;

insert into brain.settings default values;
reset role;
