"""REV-01 fix pass: the measurements behind RV-05 and RV-06, repeated on the fixed service. Prints; asserts nothing.

  measure.py scale        how one caller's latency grows with the pages OTHER organizations hold (RV-05)
  measure.py timing       forbidden page against missing page over HTTP, by id and by path (RV-06)
  measure.py timing-db    the same inside one database session, where a commit to disk adds no noise
  measure.py baseline-db  the in-database measurement on R-02's schema, for comparison. Needs SUPER_DSN and loads
                          ../r-02/service/schema.sql, so run.sh runs it first and loads the fixed schema afterwards.
  measure.py matrix       which made-up organizations' text each token can read, with two people in the service

Environment as for the tests. Standard library only. Made-up data only.
"""
import hashlib, os, pathlib, random, re, statistics, subprocess, sys, time, uuid

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "tests"))
from common import T_MGMT, T_PERSONAL, T_SIBLING, T_TOVELI, admin, call, page_id, psql, reset, rpc  # noqa: E402


def scale():
    reset()
    def med(token, tool, args, n=5):
        ts = []
        for _ in range(n):
            t0 = time.perf_counter(); ok, payload, _ = call(token, tool, args); ts.append((time.perf_counter() - t0) * 1000)
        return statistics.median(ts), payload.get("count")
    print("pages added to the sibling | toveli brain_list ms (its own count) | toveli brain_search ms | toveli brain_get own path ms | holding brain_list ms (count) | personal brain_search ms (count)")
    total = 0
    for add in [0, 250, 750, 4000, 5000]:
        if add:
            ups = [{"path": f"gen/{total + i:06d}.py", "title": f"Code: gen/{total + i:06d}.py", "body": f"made-up page {total + i}", "kind": "code_file",
                    "content_sha": hashlib.sha1(str(total + i).encode()).hexdigest()} for i in range(add)]
            admin("/admin/codebase_sync", {"org": "sibling", "upserts": ups}); total += add
        a, b, c = med(T_TOVELI, "brain_list", {"limit": 50}), med(T_TOVELI, "brain_search", {"query": "CANARY"}), med(T_TOVELI, "brain_get", {"path": "apps/example/main.ts"})
        d, e = med(T_MGMT, "brain_list", {"limit": 50}), med(T_PERSONAL, "brain_search", {"query": "made-up page 7"})
        print(f"{total:>26} | {a[0]:>10.1f} ({a[1]}) | {b[0]:>10.1f} | {c[0]:>8.1f} | {d[0]:>10.1f} ({d[1]}) | {e[0]:>10.1f} ({e[1]})")
    print("\nThe toveli columns are the finding: they must not move. The last two columns are callers who are allowed to read the sibling's pages,")
    print("so their time grows with what they are given; they are shown so that the cost of reading 10,000 pages is on the record.")
    reset()


def timing(n=1000):
    reset()
    sib = page_id(T_SIBLING, "CANARY-SIBLING-1")
    cases = {"id, sibling's page (exists, forbidden)": lambda: {"id": sib}, "id, random (missing)": lambda: {"id": str(uuid.uuid4())},
             "path, sibling's path (exists, forbidden)": lambda: {"path": "services/quant/run.py"}, "path, missing, same length": lambda: {"path": "services/quant/rux.py"}}
    samples = {k: [] for k in cases}
    def one(args):
        t0 = time.perf_counter_ns(); status, raw = rpc(T_TOVELI, "brain_get", args); dt = (time.perf_counter_ns() - t0) / 1000.0
        assert '{\\"error\\":\\"not_found\\"}' in raw, raw[:200]
        return dt
    for _ in range(40):
        for f in cases.values(): one(f())
    order = list(cases)
    for _ in range(n):
        random.shuffle(order)
        for k in order: samples[k].append(one(cases[k]()))
    print(f"caller: the toveli agent, tool brain_get, {n} interleaved samples each; every answer is the same text, {{\"error\":\"not_found\"}}")
    for k, v in samples.items():
        v = sorted(v); print(f"  {k:<42} median {statistics.median(v):7.0f} us   quartiles {v[len(v) // 4]:7.0f} to {v[3 * len(v) // 4]:7.0f}")
    for a, b in [("id, sibling's page (exists, forbidden)", "id, random (missing)"), ("path, sibling's path (exists, forbidden)", "path, missing, same length")]:
        boots = sorted(statistics.median(random.choices(samples[a], k=n)) - statistics.median(random.choices(samples[b], k=n)) for _ in range(400))
        print(f"  difference of medians, {a.split(',')[0]}: {statistics.median(samples[a]) - statistics.median(samples[b]):.0f} us (95% interval {boots[10]:.0f} to {boots[389]:.0f})")
    a, b = samples["path, sibling's path (exists, forbidden)"], samples["path, missing, same length"]
    for k in (1, 5, 15):
        right = sum(statistics.median(random.sample(a, k)) > statistics.median(random.sample(b, k)) for _ in range(2000)) / 2000
        print(f"  a guess from {k:>2} sample(s) of each path names the existing one correctly {right:.0%} of the time (50% is a coin toss)")
    reset()


def _batches(statement_forbidden, statement_missing, token, dsn=None, batches=200):
    """Median, over batches of 100 pairs, of (forbidden - missing) in microseconds, measured inside one session."""
    timed = lambda stmt, acc: f"t0 := clock_timestamp(); {stmt} {acc} := {acc} + extract(epoch from clock_timestamp() - t0) * 1e6;"
    code, out = psql(f"""begin; select brain.begin_session('{token}');
        do $$ declare t0 timestamptz; a float8; b float8; d float8[] := '{{}}'; m float8; ma float8 := 0; mb float8 := 0;
        begin
          for j in 1..{batches + 5} loop
            a := 0; b := 0;
            for i in 1..50 loop {timed(statement_forbidden, 'a')} {timed(statement_missing, 'b')} {timed(statement_missing, 'b')} {timed(statement_forbidden, 'a')} end loop;
            if j > 5 then d := d || (a - b) / 100; ma := ma + a / 100; mb := mb + b / 100; end if;
          end loop;
          select percentile_cont(0.5) within group (order by x) into m from unnest(d) x;
          raise notice 'RESULT % % %', round((ma / {batches})::numeric, 2), round((mb / {batches})::numeric, 2), round(m::numeric, 3);
        end $$; rollback;""", dsn)
    m = re.search(r"RESULT (\S+) (\S+) (\S+)", out)
    assert m, out[-400:]
    return m.groups()


def timing_db():
    reset()
    sib = page_id(T_SIBLING, "CANARY-SIBLING-1")
    get = lambda args: f"begin perform brain.t_get(null, null, {args}); exception when sqlstate 'BR404' then null; end;"
    print("inside one database session as the service's own login, bound to the toveli agent's token; 20,000 lookups of each kind, interleaved, in 200 batches")
    print("lookup | forbidden us | missing us | median batch difference us")
    for label, f, m in [("brain.t_get by path", "null, 'services/quant/run.py', null", "null, 'services/quant/rux.py', null"),
                        ("brain.t_get by id", f"'{sib}', null, null", f"'{uuid.uuid4()}', null, null")]:
        for rep in range(3):
            fa, mi, d = _batches(get(f), get(m), T_TOVELI)
            print(f"{label} | {fa} | {mi} | {d}")
    # A different question, kept apart: a parent in summaries mode asking for a note of its OWN child that it may not read.
    note = page_id(T_TOVELI, "CANARY-TOVELI-1")
    admin("/admin/settings", {"holding_reads": "summaries"})
    for rep in range(3):
        fa, mi, d = _batches(get(f"'{note}', null, null"), get(f"'{uuid.uuid4()}', null, null"), T_MGMT)
        print(f"holding organization in summaries mode, a note of its own venture, by id | {fa} | {mi} | {d}")
    print("\nThe last three rows are a known difference, not a fixed one: the venture is one the caller reads, the row is fetched, and its kind then rules it out.")
    print("It tells the layer above that some page of its own venture has that id. It tells nobody anything about an organization they do not read.")
    reset()


def baseline_db():
    """The same in-database measurement on R-02's schema, where the role selects from the table under row-level security."""
    dsn = os.environ["SUPER_DSN"]
    schema = HERE.parent / "r-02" / "service" / "schema.sql"
    out = subprocess.run(["psql", dsn, "-X", "-q", "-v", "ON_ERROR_STOP=1", "-v", "owner_pw=" + os.environ["OWNER_PW"], "-v", "app_pw=" + os.environ["APP_PW"], "-f", str(schema)],
                         capture_output=True, text=True)
    assert out.returncode == 0, out.stderr[-300:]
    token = "baseline-toveli-agent"
    code, out = psql(f"""insert into brain.orgs (id, kind, parent_id) values ('mgmt', 'holding', null), ('toveli', 'sub', 'mgmt'), ('sibling', 'sub', 'mgmt');
        insert into brain.principals values (encode(sha256(convert_to('{token}', 'UTF8')), 'hex'), 'toveli', 'agent');
        insert into brain.pages (org_id, org_kind, title, body, kind, source_type, path)
          select o, 'sub', 'Code: ' || p, 'made-up', 'code_file', 'codebase', p from (values ('toveli', 'apps/example/main.ts'), ('sibling', 'services/quant/run.py')) v (o, p);
        insert into brain.pages (org_id, org_kind, title, body) select case when i % 2 = 0 then 'toveli' else 'sibling' end, 'sub', 'note ' || i, 'made-up' from generate_series(1, 10) i;
        select 'ID=' || id from brain.pages where org_id = 'sibling' and path is not null;""", dsn)
    sib = re.search(r"ID=(\S+)", out).group(1)
    sel = lambda cond: f"perform 1 from brain.pages where {cond};"
    print("R-02's schema (spikes/r-02/service/schema.sql), 12 made-up pages, same harness; 4,000 lookups of each kind in 40 batches")
    print("lookup | forbidden us | missing us | median batch difference us")
    for label, f, m in [("select by path", "path = 'services/quant/run.py'", "path = 'services/quant/rux.py'"), ("select by id", f"id = '{sib}'", f"id = '{uuid.uuid4()}'")]:
        fa, mi, d = _batches(sel(f), sel(m), token, batches=40)
        print(f"{label} | {fa} | {mi} | {d}")


def matrix():
    from test_rev01_second_person import TOK, fixture
    admin("/admin/reset", fixture("C"))
    who = [("shared", "human"), ("shared", "agent"), ("friend-personal", "agent"), ("personal", "agent"), ("mgmt", "agent"), ("toveli", "agent"), ("acme", "agent"), ("acme-sub", "agent")]
    cols = ["SHARED", "GLOBAL", "TOVELI", "SIBLING", "MGMT", "PERSONAL", "FRIENDP", "ACME", "ACMESUB", "ACMEGLOBAL"]
    print("token of (organization/actor)".ljust(30) + " ".join(c.ljust(10) for c in cols))
    for org, actor in who:
        ok, payload, raw = call(TOK(org, actor), "brain_search", {"query": "CANARY", "limit": 200})
        got = set(re.findall(r"CANARY-([A-Z]+)-\d", raw))
        print(f"{org}/{actor}".ljust(30) + " ".join(("reads" if c in got else "-").ljust(10) for c in cols))
    print("\nColumns are whose made-up pages: SHARED the shared venture; GLOBAL and MGMT Cole's holding organization (global page, own page); TOVELI and SIBLING Cole's other ventures;")
    print("PERSONAL Cole's personal space; FRIENDP the friend's personal space; ACME, ACMESUB, ACMEGLOBAL the friend's own company.")
    print("People: Cole owns the holding organization and co-owns the shared venture. The friend co-owns the shared venture and owns the other company.")
    reset()


if __name__ == "__main__":
    {"scale": scale, "timing": timing, "timing-db": timing_db, "baseline-db": baseline_db, "matrix": matrix}[sys.argv[1]]()
