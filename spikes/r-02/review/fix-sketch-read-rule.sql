-- REV-01, finding RV-05 (and what it shows about RV-06): a sketch of the smallest fix to the read rule.
-- NOT applied to ../service/schema.sql. A sketch for the build session, not a reviewed design.
--
-- The spike's policy calls brain.can_read() once for every row the query touches, and that function runs three
-- more queries. So every list or search costs about a third of a millisecond for every page of every
-- organization (RV-05). This sketch states the same rule as plain column comparisons against values that are
-- worked out once per statement: each "(select ...)" below becomes an InitPlan.
--
-- It keeps the spike's rule exactly (one holding organization, one personal space). It does NOT fix RV-03:
-- the personal branch still reads every organization, and "global" is still global to the whole service.
--
-- Load after schema.sql, as a superuser:   psql ... -f ../service/schema.sql -f fix-sketch-read-rule.sql
--
-- Checked on 2026-11-17 (results/fix-sketch.txt), service unmodified:
--   - the 35 existing tests still pass;
--   - RV-05 is fixed: with 10,000 pages in the sibling, toveli's list takes 8 ms (2,853 ms without the sketch);
--   - RV-06 is NOT fixed: a forbidden page still answers about 0.4 ms slower than a missing one. PostgreSQL
--     runs an InitPlan only when a row first needs it, so the session lookups (0.7 ms in the database) happen
--     when a row of another organization is found and do not happen when no row is found. Closing that needs
--     the lookup to run on every call whether or not a row matches. Not built here;
--   - no other result of the review's tests changes (14 of 24 and 8 of 13 still fail).

set role brain_owner;

-- The organizations a holding organization reads in full (holding_reads = 'all'): its own children.
create function brain.rr_children_all() returns text[]
language sql stable security definer set search_path = brain, pg_temp as $$
  select case when brain.current_kind() = 'holding' and (select holding_reads from brain.settings) = 'all'
              then array(select id from brain.orgs where parent_id = brain.current_org())
              else '{}'::text[] end
$$;

-- The organizations a holding organization reads summaries of (holding_reads = 'summaries').
create function brain.rr_children_summaries() returns text[]
language sql stable security definer set search_path = brain, pg_temp as $$
  select case when brain.current_kind() = 'holding' and (select holding_reads from brain.settings) = 'summaries'
              then array(select id from brain.orgs where parent_id = brain.current_org())
              else '{}'::text[] end
$$;

-- The organizations a personal space reads. The spike's rule: all of them (this is RV-03, kept as it is here).
create function brain.rr_person_orgs() returns text[]
language sql stable security definer set search_path = brain, pg_temp as $$
  select case when brain.current_kind() = 'personal'
              then array(select id from brain.orgs where kind <> 'personal')
              else '{}'::text[] end
$$;

revoke all on function brain.rr_children_all(), brain.rr_children_summaries(), brain.rr_person_orgs() from public;
grant execute on function brain.rr_children_all(), brain.rr_children_summaries(), brain.rr_person_orgs() to brain_app;

drop policy pages_read on brain.pages;
create policy pages_read on brain.pages for select to brain_app using (
  (kind <> 'briefing' or (select brain.feature('briefing')))                    -- switch off hides earlier briefings
  and (
    org_id = (select brain.current_org())                                       -- own pages; null when no session is bound
    or (org_kind <> 'personal' and (                                            -- nobody else reads personal
          (visibility = 'global' and (select brain.current_org()) is not null)  -- shared on purpose by the holding organization
       or org_id = any ((select brain.rr_person_orgs())::text[])                -- the person reads their organizations
       or org_id = any ((select brain.rr_children_all())::text[])               -- the layer above reads what is below it
       or (kind = 'summary' and org_id = any ((select brain.rr_children_summaries())::text[]))
    ))
  )
);

reset role;
