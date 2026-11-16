"""Criterion 8, two checks on the real map:
1. A new commit updates the map without a full rebuild, and the result equals a full rebuild.
2. A sibling organization cannot read Toveli's code pages.

  test_incremental.py <repo> <old commit> <new commit> <scratch dir>
Needs BRAIN_SOCKET (or host/port) and BRAIN_ADMIN_TOKEN. Prints a JSON report; exit code 1 if a check fails.
"""
import json, pathlib, sys, time
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
import map_repo
from brainclient import Brain
from sync_brain import sync

repo, old_c, new_c, scratch = sys.argv[1], sys.argv[2], sys.argv[3], pathlib.Path(sys.argv[4])
fixture = json.loads((pathlib.Path(__file__).resolve().parent.parent / "tests" / "fixture.json").read_text())
tok = {(p["org"], p["actor"]): p["token"] for p in fixture["principals"]}
brain, report, ok = Brain(), {}, True
brain.admin("POST", "/admin/reset", fixture)

t0 = time.time(); m_old = map_repo.build(repo, old_c); t_full_old = time.time() - t0
report["full_build_old"] = {**m_old["stats"], "deleted": 0, "seconds": round(t_full_old, 2), "commit": m_old["commit"][:7], "sync": sync(m_old, "toveli", brain)}
before = {r["path"]: r for r in brain.admin("GET", "/admin/pages_digest?org=toveli&source_type=codebase")["rows"]}

time.sleep(1.1)
t0 = time.time(); m_inc = map_repo.build(repo, new_c, old=m_old); t_inc = time.time() - t0
s_inc = sync(m_inc, "toveli", brain)
after = {r["path"]: r for r in brain.admin("GET", "/admin/pages_digest?org=toveli&source_type=codebase")["rows"]}
report["incremental_to_new"] = {**m_inc["stats"], "deleted": len(m_inc["stats"]["deleted"]), "seconds": round(t_inc, 2), "commit": m_inc["commit"][:7], "sync": s_inc}

t0 = time.time(); m_full = map_repo.build(repo, new_c); t_full = time.time() - t0
want = {p["path"]: p["content_sha"] for p in map_repo.pages(m_full)}
got = {p: r["content_sha"] for p, r in after.items()}
touched = sorted(p for p in after if p not in before or after[p]["updated_at"] != before[p]["updated_at"])
untouched_same = all(after[p]["content_sha"] == before[p]["content_sha"] for p in after if p in before and p not in touched)
report["full_build_new"] = {**m_full["stats"], "deleted": 0, "seconds": round(t_full, 2)}
report["checks"] = {
    "incremental result equals a full rebuild (every page, by content hash)": got == want,
    "incremental read fewer files than a full build": m_inc["stats"]["files_read"] < m_full["stats"]["files_read"],
    "pages rewritten equals pages whose content changed": len(touched) == s_inc["written"],
    "pages that did not change were not rewritten": untouched_same and s_inc["pages_unchanged"] > 0,
}
report["pages_rewritten"] = len(touched); report["pages_total"] = len(after)
json.dump(m_full, open(scratch / f"manifest-{m_full['commit'][:7]}.json", "w"))

# the sibling organization and the real code pages
sib, tov, mgmt = tok[("sibling", "agent")], tok[("toveli", "agent")], tok[("mgmt", "agent")]
ok_t, lst_t = brain.tool(tov, "brain_list", {"source_type": "codebase", "limit": 200})
ok_s, lst_s = brain.tool(sib, "brain_list", {"source_type": "codebase", "limit": 200})
probes = []
for args in [{"path": "/"}, {"path": "apps/api/src/main.ts"}, {"path": "packages/db/src/migrate.ts"}]:
    probes.append(brain.tool(sib, "brain_get", args)[0])
searches = [brain.tool(sib, "brain_search", {"query": q, "limit": 50})[1] for q in ["buildApp", "@toveli/db", "pnpm db:migrate", "apps/api", "Codebase overview"]]
leaked = [p for s in searches for p in s.get("pages", []) if p["org"] == "toveli"]
ok_m, lst_m = brain.tool(mgmt, "brain_get", {"path": "apps/api/src/main.ts"})
report["sibling"] = {"toveli agent lists code pages": lst_t.get("count"), "sibling agent lists code pages": lst_s.get("count"),
                     "sibling page orgs": sorted({p["org"] for p in lst_s.get("pages", [])})}
report["checks"].update({
    "Toveli's own agent can list the code pages": ok_t and lst_t.get("count") == len(want),
    "sibling sees no Toveli code page in a list": ok_s and all(p["org"] != "toveli" for p in lst_s.get("pages", [])),
    "sibling cannot fetch a Toveli code page by path": not any(probes),
    "sibling search returns no Toveli code page": not leaked,
    "holding organization can read the code page (holding_reads = all, the current rule)": ok_m,
})
ok = all(report["checks"].values())
print(json.dumps(report, indent=1))
sys.exit(0 if ok else 1)
