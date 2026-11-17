"""Write a manifest's pages into an organization's second brain, tagged as codebase. Only changed pages are written.

  sync_brain.py <manifest.json> <org>        (BRAIN_SOCKET or BRAIN host/port, BRAIN_ADMIN_TOKEN in the environment)
"""
import json, sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
import map_repo
from brainclient import Brain


def sync(manifest, org, brain=None):
    brain = brain or Brain()
    pages = map_repo.pages(manifest)
    have = {r["path"]: r["content_sha"] for r in brain.admin("GET", f"/admin/pages_digest?org={org}&source_type=codebase")["rows"]}
    want = {p["path"]: p["content_sha"] for p in pages}
    changed = [p for p in pages if have.get(p["path"]) != p["content_sha"]]
    deletes = sorted(set(have) - set(want))
    out = {"written": 0, "deleted": 0}
    for i in range(0, len(changed), 100):
        r = brain.admin("POST", "/admin/codebase_sync", {"org": org, "upserts": changed[i:i + 100], "deletes": []})
        out["written"] += r["written"]
    if deletes:
        out["deleted"] = brain.admin("POST", "/admin/codebase_sync", {"org": org, "upserts": [], "deletes": deletes})["deleted"]
    out.update(pages_total=len(pages), pages_unchanged=len(pages) - len(changed))
    return out


if __name__ == "__main__":
    print(json.dumps(sync(json.load(open(sys.argv[1])), sys.argv[2])))
