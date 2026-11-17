"""REV-01: two measurements behind findings RV-05 and RV-06, and the read matrix behind item 9. Prints; asserts nothing.

  measure.py scale     how one caller's latency grows with the pages OTHER organizations hold
  measure.py timing    forbidden page against missing page, by id and by path (same answer text)
  measure.py matrix    which made-up organizations' text each token can read, with two people in the service

Environment as for the tests. Standard library only. Made-up data only.
"""
import hashlib, random, re, statistics, sys, time, uuid

from common import T_MGMT, T_SIBLING, T_TOVELI, admin, call, page_id, reset, rpc


def scale():
    reset()
    def med(token, tool, args, n=5):
        ts = []
        for _ in range(n):
            t0 = time.perf_counter(); ok, payload, _ = call(token, tool, args); ts.append((time.perf_counter() - t0) * 1000)
        return statistics.median(ts), payload.get("count")
    print("pages added to the sibling | toveli brain_list ms (its own count) | toveli brain_search ms | toveli brain_get own path ms | holding brain_list ms (count)")
    total = 0
    for add in [0, 250, 750, 4000, 5000]:
        if add:
            ups = [{"path": f"gen/{total + i:06d}.py", "title": f"Code: gen/{total + i:06d}.py", "body": f"made-up page {total + i}", "kind": "code_file",
                    "content_sha": hashlib.sha1(str(total + i).encode()).hexdigest()} for i in range(add)]
            admin("/admin/codebase_sync", {"org": "sibling", "upserts": ups}); total += add
        a, b, c, d = med(T_TOVELI, "brain_list", {"limit": 50}), med(T_TOVELI, "brain_search", {"query": "CANARY"}), med(T_TOVELI, "brain_get", {"path": "apps/example/main.ts"}), med(T_MGMT, "brain_list", {"limit": 50})
        print(f"{total:>26} | {a[0]:>10.1f} ({a[1]}) | {b[0]:>10.1f} | {c[0]:>8.1f} | {d[0]:>10.1f} ({d[1]})")
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
    # how many samples does one guess need? classify single pairs by which was slower
    a, b = samples["path, sibling's path (exists, forbidden)"], samples["path, missing, same length"]
    for k in (1, 5, 15):
        right = sum(statistics.median(random.sample(a, k)) > statistics.median(random.sample(b, k)) for _ in range(2000)) / 2000
        print(f"  a guess from {k:>2} sample(s) of each path names the existing one correctly {right:.0%} of the time")
    reset()


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
    reset()


if __name__ == "__main__":
    {"scale": scale, "timing": timing, "matrix": matrix}[sys.argv[1]]()
