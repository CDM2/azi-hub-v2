"""REV-01: which deliberate breaks of schema.sql do the 35 existing tests notice?

R-02 reports two deliberate breaks (the read rule returns true; the application role may bypass
row-level security). This runs more, one at a time: each mutant is a copy of ../service/schema.sql
with one rule weakened. The copy is loaded into the local database, ../tests/test_criteria_1_3.py is
run against the unmodified service, and the result is recorded as "killed" (at least one test failed)
or "SURVIVED" (all 35 passed although a rule was gone). The original schema is loaded again at the end.
Nothing under ../service or ../tests is changed.

Run through run.sh, or:  python3 mutation_sweep.py   with SUPER_DSN, BRAIN_URL, BRAIN_ADMIN_TOKEN, BRAIN_APP_DSN,
OWNER_PW and APP_PW set (see run.sh). Standard library only.
"""
import os, pathlib, re, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).resolve().parent
SCHEMA = (HERE.parent / "service" / "schema.sql").read_text()
TESTS = HERE.parent / "tests"
SUPER_DSN = os.environ["SUPER_DSN"]

# (name, what is weakened, text to find, replacement). Each "find" must occur exactly once.
MUTANTS = [
    ("M01", "read rule: the line that keeps personal pages from other callers is removed",
     "    when p_org_kind = 'personal' then false                          -- nobody else reads personal\n", ""),
    ("M02", "read rule: a holding organization reads every sub-organization, not only its own children",
     "exists (select 1 from brain.orgs c where c.id = p_org and c.parent_id = me.org)",
     "exists (select 1 from brain.orgs c where c.id = p_org and c.kind = 'sub')"),
    ("M03", "read rule: the briefing switch no longer hides earlier briefings",
     "    when p_kind = 'briefing' and not s.briefing_enabled then false   -- switch off hides earlier briefings\n", ""),
    ("M04", "read rule: in summaries mode the holding organization also reads notes",
     "then (s.holding_reads = 'all' or p_kind = 'summary')", "then (s.holding_reads = 'all' or p_kind in ('summary', 'note'))"),
    ("M05", "read rule: a sub-organization reads its parent's pages (not only global ones)",
     "    when p_visibility = 'global' then true                           -- shared on purpose by the holding organization\n",
     "    when p_visibility = 'global' then true\n    when exists (select 1 from brain.orgs c where c.id = me.org and c.parent_id = p_org) then true\n"),
    ("M06", "write rule: an agent may add a page of any kind (for example a forged 'briefing' or code page)",
     "              and kind in ('note', 'summary')\n", ""),
    ("M07", "write rule: an agent may set a path (and so collide with or imitate codebase pages)",
     "              and path is null\n", ""),
    ("M08", "write rule: provenance is no longer forced from the caller's kind",
     "              and source_type = case brain.current_actor() when 'human' then 'human' else 'agent' end);", ");"),
    ("M09", "constraint removed: any organization may publish a global page",
     ",\n  constraint only_holding_publishes_global check (visibility = 'org' or org_kind = 'holding')", ""),
    ("M10", "constraint removed: health and finance pages may be stored outside personal",
     "  constraint health_and_finance_stay_personal check (sensitivity = 'normal' or org_kind = 'personal'),\n", ""),
    ("M11", "briefing rule: any organization may publish a briefing (database side)",
     "              and brain.current_kind() = 'personal'\n", ""),
    ("M12", "briefing rule: an agent may insert a briefing that is already marked approved",
     "              and status = 'pending' and approved_by is null and approved_at is null and page_id is null);", ");"),
    ("M13", "briefing rule: the briefing switch is not checked when publishing (database side)",
     "              and brain.feature('briefing')\n", ""),
    ("M14", "session: the personal-space switch is not checked when a token is presented",
     "     and (o.kind <> 'personal' or (select s.personal_enabled from brain.settings s));", ";"),
    ("M15", "session: a bound session outlives its transaction (current_org ignores the transaction id)",
     "$$ select org_id from brain.sessions where pid = pg_backend_pid() and txid = txid_current_if_assigned() $$;",
     "$$ select org_id from brain.sessions where pid = pg_backend_pid() $$;"),
    ("M16", "audit: the append-only triggers are not created",
     "create trigger audit_no_change before update or delete on brain.audit\n  for each row execute function brain.audit_is_append_only();\n"
     "create trigger audit_no_truncate before truncate on brain.audit\n  for each statement execute function brain.audit_is_append_only();\n", ""),
    ("M17", "privileges: the application role may read the audit log and the token table",
     "insert into brain.settings default values;", "grant select on brain.audit, brain.principals to brain_app;\ninsert into brain.settings default values;"),
    ("M18", "privileges: the application role may update and delete pages (with a permissive policy for its own organization)",
     "insert into brain.settings default values;",
     "grant update, delete on brain.pages to brain_app;\ncreate policy pages_change on brain.pages for update to brain_app using (org_id = brain.current_org());\n"
     "create policy pages_remove on brain.pages for delete to brain_app using (org_id = brain.current_org());\ninsert into brain.settings default values;"),
    ("M19", "read rule: the personal space reads only global pages and its own (it no longer reads its organizations)",
     "    when me.kind = 'personal' then true                              -- the person reads their organizations\n", ""),
]


def load(sql_text):
    with tempfile.NamedTemporaryFile("w", suffix=".sql", delete=False) as f:
        f.write(sql_text)
    out = subprocess.run(["psql", SUPER_DSN, "-X", "-q", "-v", "ON_ERROR_STOP=1", "-v", "owner_pw=" + os.environ["OWNER_PW"],
                          "-v", "app_pw=" + os.environ["APP_PW"], "-f", f.name], capture_output=True, text=True)
    os.unlink(f.name)
    return out.returncode, out.stderr.strip()[-300:]


def run_tests():
    out = subprocess.run([sys.executable, "-m", "unittest", "test_criteria_1_3"], cwd=TESTS, capture_output=True, text=True,
                         env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    text = out.stdout + out.stderr
    ran = re.search(r"Ran (\d+) tests", text)
    failed = re.findall(r"^(?:FAIL|ERROR): (\S+)", text, re.M)
    return int(ran.group(1)) if ran else 0, failed


def main():
    rc, err = load(SCHEMA)
    assert rc == 0, err
    ran, failed = run_tests()
    print(f"baseline: ran {ran}, failed {len(failed)}")
    assert ran == 35 and not failed, "the unmodified schema must pass all 35 tests before any mutant is tried"
    survived = []
    for name, what, find, repl in MUTANTS:
        assert SCHEMA.count(find) == 1, f"{name}: the text to replace occurs {SCHEMA.count(find)} times"
        rc, err = load(SCHEMA.replace(find, repl))
        if rc != 0:
            print(f"{name}  NOT LOADED  {what}  ({err})")
            continue
        ran, failed = run_tests()
        verdict = "killed  " if failed else "SURVIVED"
        if not failed:
            survived.append(name)
        print(f"{name}  {verdict}  ran {ran}, failed {len(failed):2d}  {what}" + (f"  [first: {failed[0]}]" if failed else ""))
    rc, err = load(SCHEMA)
    assert rc == 0, err
    ran, failed = run_tests()
    print(f"restored: ran {ran}, failed {len(failed)}")
    print(f"mutants: {len(MUTANTS)}; killed {len(MUTANTS) - len(survived)}; survived {len(survived)}: {', '.join(survived) or 'none'}")


if __name__ == "__main__":
    main()
