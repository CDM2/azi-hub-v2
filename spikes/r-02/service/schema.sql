-- R-02 spike: the permission service's database. Run as a superuser:
--   psql -v ON_ERROR_STOP=1 -v owner_pw=... -v app_pw=... -f schema.sql
--
-- Two roles. brain_owner owns the objects and stands in for the human's console.
-- brain_app is what agent calls run as: it owns nothing, cannot bypass row-level
-- security, and can only learn which organization it acts for by presenting a token
-- to brain.begin_session(). The organization is therefore decided inside the database.

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

create table brain.settings (
  id boolean primary key default true check (id),
  personal_enabled boolean not null default true,
  briefing_enabled boolean not null default true,
  holding_reads text not null default 'all' check (holding_reads in ('all', 'summaries'))
);

-- The tier map. A sub-organization has a parent; a holding organization and the personal space do not.
create table brain.orgs (
  id text primary key,
  kind text not null check (kind in ('personal', 'holding', 'sub')),
  parent_id text references brain.orgs (id),
  unique (id, kind),
  check ((kind = 'sub') = (parent_id is not null))
);

create table brain.principals (
  token_sha256 text primary key,
  org_id text not null references brain.orgs (id) on delete cascade,
  actor text not null check (actor in ('agent', 'human'))
);

-- Which organization the current transaction acts for. Written only by begin_session().
create table brain.sessions (
  pid int primary key,
  txid bigint not null,
  org_id text not null,
  actor text not null
);

create table brain.pages (
  id uuid primary key default gen_random_uuid(),
  org_id text not null,
  org_kind text not null,
  title text not null check (char_length(title) between 1 and 300),
  body text not null default '',
  kind text not null default 'note' check (kind in ('note', 'summary', 'briefing', 'code_file', 'code_package', 'code_overview')),
  source_type text not null default 'agent' check (source_type in ('human', 'agent', 'codebase')),
  sensitivity text not null default 'normal' check (sensitivity in ('normal', 'health', 'finance')),
  visibility text not null default 'org' check (visibility in ('org', 'global')),
  path text,
  content_sha text,
  meta jsonb not null default '{}',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  foreign key (org_id, org_kind) references brain.orgs (id, kind) on delete cascade,
  constraint health_and_finance_stay_personal check (sensitivity = 'normal' or org_kind = 'personal'),
  constraint only_holding_publishes_global check (visibility = 'org' or org_kind = 'holding')
);
create unique index pages_org_path on brain.pages (org_id, path) where path is not null;

create table brain.briefings (
  id uuid primary key default gen_random_uuid(),
  from_org text not null references brain.orgs (id) on delete cascade,
  to_org text not null references brain.orgs (id) on delete cascade,
  content text not null check (char_length(content) between 1 and 2000),
  status text not null default 'pending' check (status in ('pending', 'approved', 'rejected')),
  created_at timestamptz not null default now(),
  approved_by text,
  approved_at timestamptz,
  page_id uuid
);

create table brain.audit (
  id bigserial primary key,
  ts timestamptz not null default now(),
  org text,
  actor text,
  tool text not null,
  request_id text,
  decision text not null check (decision in ('allow', 'deny')),
  reason text,
  args_sha256 text
);
create function brain.audit_is_append_only() returns trigger language plpgsql as
$$ begin raise exception 'the audit log is append-only'; end $$;
create trigger audit_no_change before update or delete on brain.audit
  for each row execute function brain.audit_is_append_only();
create trigger audit_no_truncate before truncate on brain.audit
  for each statement execute function brain.audit_is_append_only();

-- Session binding -------------------------------------------------------------------------------

create function brain.begin_session(p_token text) returns table (org text, kind text, actor text)
language plpgsql security definer set search_path = brain, pg_temp as $$
declare v record;
begin
  select pr.org_id, o.kind, pr.actor into v
    from brain.principals pr join brain.orgs o on o.id = pr.org_id
   where pr.token_sha256 = encode(sha256(convert_to(coalesce(p_token, ''), 'UTF8')), 'hex')
     and (o.kind <> 'personal' or (select s.personal_enabled from brain.settings s));
  if not found then
    raise exception 'invalid_token' using errcode = '28000';
  end if;
  insert into brain.sessions (pid, txid, org_id, actor)
  values (pg_backend_pid(), txid_current(), v.org_id, v.actor)
  on conflict (pid) do update set txid = excluded.txid, org_id = excluded.org_id, actor = excluded.actor;
  return query select v.org_id::text, v.kind::text, v.actor::text;
end $$;

create function brain.current_org() returns text
language sql stable security definer set search_path = brain, pg_temp as
$$ select org_id from brain.sessions where pid = pg_backend_pid() and txid = txid_current_if_assigned() $$;

create function brain.current_actor() returns text
language sql stable security definer set search_path = brain, pg_temp as
$$ select actor from brain.sessions where pid = pg_backend_pid() and txid = txid_current_if_assigned() $$;

create function brain.current_kind() returns text
language sql stable security definer set search_path = brain, pg_temp as
$$ select kind from brain.orgs where id = brain.current_org() $$;

create function brain.holding_org() returns text
language sql stable security definer set search_path = brain, pg_temp as
$$ select id from brain.orgs where kind = 'holding' order by id limit 1 $$;

create function brain.feature(p_name text) returns boolean
language sql stable security definer set search_path = brain, pg_temp as
$$ select case p_name when 'personal' then personal_enabled when 'briefing' then briefing_enabled end from brain.settings $$;

-- The read rule, in one place ---------------------------------------------------------------------

create function brain.can_read(p_org text, p_org_kind text, p_kind text, p_visibility text) returns boolean
language sql stable security definer set search_path = brain, pg_temp as $$
  select case
    when me.org is null then false                                   -- no bound session: nothing
    when p_kind = 'briefing' and not s.briefing_enabled then false   -- switch off hides earlier briefings
    when p_org = me.org then true                                    -- own pages
    when p_org_kind = 'personal' then false                          -- nobody else reads personal
    when p_visibility = 'global' then true                           -- shared on purpose by the holding organization
    when me.kind = 'personal' then true                              -- the person reads their organizations
    when me.kind = 'holding'
         and exists (select 1 from brain.orgs c where c.id = p_org and c.parent_id = me.org)
      then (s.holding_reads = 'all' or p_kind = 'summary')           -- the layer above reads what is below it
    else false                                                       -- siblings and everything else
  end
  from (select brain.current_org() as org, brain.current_kind() as kind) me, brain.settings s
$$;

alter table brain.pages enable row level security;
alter table brain.pages force row level security;
create policy pages_read on brain.pages for select to brain_app
  using (brain.can_read(org_id, org_kind, kind, visibility));
-- An agent or a person adds notes and summaries to their own organization only. Provenance follows the caller.
create policy pages_add on brain.pages for insert to brain_app
  with check (org_id = brain.current_org()
              and org_kind = brain.current_kind()
              and kind in ('note', 'summary')
              and path is null
              and source_type = case brain.current_actor() when 'human' then 'human' else 'agent' end);
create policy pages_console on brain.pages for all to brain_owner using (true) with check (true);

alter table brain.briefings enable row level security;
alter table brain.briefings force row level security;
create policy briefings_own on brain.briefings for select to brain_app using (from_org = brain.current_org());
create policy briefings_publish on brain.briefings for insert to brain_app
  with check (from_org = brain.current_org()
              and brain.current_kind() = 'personal'
              and brain.feature('briefing')
              and to_org = brain.holding_org()
              and status = 'pending' and approved_by is null and approved_at is null and page_id is null);
create policy briefings_console on brain.briefings for all to brain_owner using (true) with check (true);

-- Audit: agents can only append, through this function, and the row is stamped from the bound session.
create function brain.audit_log(p_tool text, p_request_id text, p_decision text, p_reason text, p_args_sha text) returns void
language sql security definer set search_path = brain, pg_temp as $$
  insert into brain.audit (org, actor, tool, request_id, decision, reason, args_sha256)
  values (brain.current_org(), brain.current_actor(), left(p_tool, 60), left(p_request_id, 100), p_decision, left(p_reason, 100), left(p_args_sha, 64))
$$;

-- Human approval of a briefing. Runs as the console role only.
create function brain.approve_briefing(p_id uuid, p_approver text) returns uuid
language plpgsql set search_path = brain, pg_temp as $$
declare b brain.briefings; v_page uuid;
begin
  if not brain.feature('briefing') then raise exception 'briefings are switched off'; end if;
  select * into b from brain.briefings where id = p_id and status = 'pending' for update;
  if not found then raise exception 'no pending briefing %', p_id; end if;
  insert into brain.pages (org_id, org_kind, title, body, kind, source_type)
  values (b.to_org, 'holding', 'Briefing from the personal space, ' || to_char(now(), 'YYYY-MM-DD'), b.content, 'briefing', 'human')
  returning id into v_page;
  update brain.briefings set status = 'approved', approved_by = p_approver, approved_at = now(), page_id = v_page where id = p_id;
  return v_page;
end $$;

-- Privileges: start from nothing.
revoke all on all tables in schema brain from public, brain_app;
revoke all on all functions in schema brain from public, brain_app;
grant usage on schema brain to brain_app;
grant select, insert on brain.pages to brain_app;
grant select, insert on brain.briefings to brain_app;
grant execute on function brain.begin_session(text), brain.current_org(), brain.current_actor(), brain.current_kind(),
  brain.holding_org(), brain.feature(text), brain.can_read(text, text, text, text),
  brain.audit_log(text, text, text, text, text) to brain_app;

insert into brain.settings default values;
reset role;
