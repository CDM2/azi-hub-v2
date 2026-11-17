"""R-02 spike, criterion 8: the smallest codebase mapper.

Deterministic. No model calls, no dependencies beyond git and the Python standard library.
It reads a repository at one commit through git plumbing (no checkout, nothing written to the
repository) and produces a manifest: for every tracked file its role, purpose, imports, importers,
exports and tests; for every workspace package its scripts and dependencies; and one overview of
how the repository builds, tests and deploys. `pages()` turns the manifest into second-brain pages.

  map_repo.py full  <repo> <commit> <manifest.json>
  map_repo.py incr  <repo> <commit> <old-manifest.json> <manifest.json>     re-reads only changed files

Purpose text comes from the file itself (its leading comment, first heading or first SQL comment).
Where a file says nothing about itself, the page says so; nothing is invented.
"""
import hashlib, json, posixpath, re, subprocess, sys

CODE_EXT = (".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs")
MAPPER_VERSION = "r02-1"


def git(repo, *args, binary=False):
    out = subprocess.run(["git", "-C", repo, *args], capture_output=True, check=True).stdout
    return out if binary else out.decode("utf-8", "replace")


def ls_tree(repo, commit):
    """{path: blob sha} for every tracked file at the commit."""
    files = {}
    for line in git(repo, "ls-tree", "-r", "-z", commit).split("\0"):
        if not line:
            continue
        meta, path = line.split("\t", 1)
        mode, kind, sha = meta.split()
        if kind == "blob":
            files[path] = sha
    return files


def read_blob(repo, sha):
    return git(repo, "cat-file", "-p", sha, binary=True)


def role_of(path):
    name = posixpath.basename(path)
    if path.startswith(".github/workflows/"):
        return "ci workflow"
    if re.search(r"\.(test|spec)\.[tj]sx?$", path) or "/__tests__/" in path:
        return "test"
    if path.endswith(".sql"):
        return "database migration"
    if "/migrations/meta/" in path:
        return "migration metadata"
    if path.endswith(".md"):
        return "document"
    if name in ("pnpm-lock.yaml", "package-lock.json", "devcontainer-lock.json"):
        return "lockfile"
    if path.endswith(CODE_EXT):
        return "config" if re.search(r"(^|/)[\w.-]*config\.[cm]?[tj]s$", path) else "source"
    if path.endswith((".png", ".jpg", ".svg", ".xlsx", ".ico")):
        return "asset"
    return "config"


def clean_comment(text):
    lines = [re.sub(r"^\s*(/\*\*?|\*/|\*|//|--|#)\s?", "", l).rstrip() for l in text.splitlines()]
    para = []
    for l in lines:
        if not l.strip():
            if para:
                break
            continue
        para.append(l.strip())
    return re.sub(r"\s+", " ", " ".join(para)).strip()[:420]


def purpose_of(path, text):
    """The file's own words about itself, or ''."""
    if path.endswith(CODE_EXT):
        m = re.search(r"/\*\*(.*?)\*/", text[:6000], re.S)          # first doc comment near the top
        if m:
            return clean_comment(m.group(1))
        head = []
        for l in text.splitlines()[:30]:
            if l.strip().startswith("//"):
                head.append(l)
            elif head:
                break
        return clean_comment("\n".join(head)) if head else ""
    if path.endswith(".md"):
        title = re.search(r"^#\s+(.+)$", text, re.M)
        body = re.sub(r"^#.*$", "", text, flags=re.M)
        first = next((p.strip() for p in re.split(r"\n\s*\n", body) if p.strip() and not p.strip().startswith(("|", "```", "---"))), "")
        return ((title.group(1).strip() + ". ") if title else "") + re.sub(r"\s+", " ", first)[:300]
    if path.endswith(".sql"):
        head = [l for l in text.splitlines()[:25] if l.strip().startswith("--")]
        return clean_comment("\n".join(head))
    if path.endswith((".yml", ".yaml", ".sh", ".gitignore", ".npmrc", ".prettierignore")) or posixpath.basename(path) in ("CODEOWNERS", "Dockerfile", ".editorconfig", ".env.example"):
        head = []
        for l in text.splitlines()[:25]:
            if l.strip().startswith("#") and not l.startswith("#!"):
                head.append(l)
            elif head:
                break
        return clean_comment("\n".join(head))
    return ""


IMPORT_RE = re.compile(r"""(?:^|[\s;])(?:import|export)\s+(?:type\s+)?(?:[^'";]*?\sfrom\s+)?['"]([^'"]+)['"]|(?:import|require)\(\s*['"]([^'"]+)['"]\s*\)""", re.M)
EXPORT_DECL_RE = re.compile(r"^export\s+(?:default\s+)?(?:declare\s+)?(?:abstract\s+)?(?:async\s+)?(?:function\*?|class|const|let|var|interface|type|enum)\s+([A-Za-z_$][\w$]*)", re.M)
EXPORT_LIST_RE = re.compile(r"^export\s+(?:type\s+)?\{([^}]*)\}", re.M | re.S)


def extract_code(text):
    specs = sorted({a or b for a, b in IMPORT_RE.findall(text)})
    exports = set(EXPORT_DECL_RE.findall(text))
    for group in EXPORT_LIST_RE.findall(text):
        for item in group.split(","):
            item = re.sub(r"^\s*type\s+", "", item.strip())
            if item:
                exports.add(item.split(" as ")[-1].strip())
    if re.search(r"^export\s+default\b", text, re.M):
        exports.add("default")
    return specs, sorted(exports)


def extract_file(repo, path, sha):
    """Everything read from one file. This is the only function that opens file content."""
    raw = read_blob(repo, sha)
    rec = {"path": path, "sha": sha, "bytes": len(raw), "role": role_of(path)}
    if rec["role"] in ("asset", "lockfile", "migration metadata") or b"\0" in raw[:2000]:
        return rec
    text = raw.decode("utf-8", "replace")
    rec["lines"] = text.count("\n") + 1
    rec["purpose"] = purpose_of(path, text)
    if path.endswith(CODE_EXT):
        rec["import_specs"], rec["exports"] = extract_code(text)
        marks = []
        if re.search(r"\.listen\(", text):
            marks.append("starts a network listener")
        if "registerRootComponent(" in text:
            marks.append("registers the mobile root component")
        if re.search(r"process\.exit\(|import\.meta\.url\s*===|process\.argv\[", text):
            marks.append("runs as a script")
        rec["marks"] = marks
    elif path.endswith(".sql"):
        rec["tables_created"] = re.findall(r"CREATE TABLE(?: IF NOT EXISTS)?\s+([\w.\"]+)", text)
    elif posixpath.basename(path) == "package.json":
        try:
            p = json.loads(text)
            rec["package"] = {k: p.get(k) for k in ("name", "version", "description", "main", "packageManager", "engines", "scripts") if p.get(k) is not None}
            rec["package"]["dependencies"] = {**p.get("dependencies", {}), **p.get("devDependencies", {}), **p.get("peerDependencies", {})}
            rec["package"]["has_exports"] = "exports" in p
        except ValueError:
            pass
    elif path.startswith(".github/workflows/"):
        rec["workflow"] = parse_workflow(text)
    elif posixpath.basename(path) == ".nvmrc":
        rec["pin"] = text.strip()
    elif posixpath.basename(path) == "eas.json":
        try:
            rec["eas_profiles"] = list(json.loads(text).get("build", {}).keys())
        except ValueError:
            pass
    elif posixpath.basename(path) == ".env.example":
        rec["env_keys"] = re.findall(r"^\s*#?\s*([A-Z][A-Z0-9_]{2,})=", text, re.M)
    elif "docker-compose" in path or posixpath.basename(path) == "Dockerfile":
        rec["images"] = sorted(set(re.findall(r"^\s*(?:image:|FROM)\s+(\S+)", text, re.M)))
    return rec


def parse_workflow(text):
    """A line-based reading of a GitHub Actions file: its name, triggers, jobs, service images and run steps."""
    wf = {"name": (re.search(r"^name:\s*(.+)$", text, re.M) or [None, ""])[1].strip(), "jobs": []}
    wf["triggers"] = re.findall(r"^  (push|pull_request|workflow_dispatch|schedule|release):", text, re.M)
    jobs = re.search(r"^jobs:\s*$", text, re.M)
    if not jobs:
        return wf
    for block in re.split(r"^  (?=[\w-]+:\s*$)", text[jobs.end():], flags=re.M)[1:]:
        job_id = block.split(":", 1)[0]
        name = re.search(r"^    name:\s*(.+)$", block, re.M)
        runs = [re.sub(r"\s+", " ", r).strip() for r in re.findall(r"^\s+run:\s*(?!\|)(.+)$", block, re.M)]
        for multi in re.findall(r"^\s+run:\s*\|\s*\n((?:\s{10,}.*\n?)+)", block, re.M):
            runs.append(" ; ".join(l.strip() for l in multi.splitlines() if l.strip()))
        wf["jobs"].append({"id": job_id, "name": name.group(1).strip() if name else job_id,
                           "images": sorted(set(re.findall(r"image:\s*(\S+)", block))), "runs": runs,
                           "uses": sorted(set(re.findall(r"uses:\s*(\S+)", block)))})
    return wf


# ----------------------------------------------------------------------------- derive (no file reads)

def derive(files):
    """Resolve imports, reverse them, group by workspace, and describe build and deploy. Pure function of the per-file records."""
    recs = {r["path"]: r for r in files}
    paths = set(recs)
    packages = {}
    for r in files:
        if posixpath.basename(r["path"]) == "package.json" and "package" in r:
            packages[posixpath.dirname(r["path"])] = r["package"]
    ws_dirs = sorted((d for d in packages if d), key=len, reverse=True)
    by_name = {p["name"]: d for d, p in packages.items() if p.get("name")}

    def workspace_of(path):
        return next((d for d in ws_dirs if path.startswith(d + "/")), "")

    def resolve(frm, spec):
        if spec.startswith("."):
            base = posixpath.normpath(posixpath.join(posixpath.dirname(frm), spec))
            for cand in [base] + [base + e for e in CODE_EXT] + [posixpath.join(base, "index" + e) for e in CODE_EXT] + [re.sub(r"\.js$", ".ts", base)]:
                if cand in paths:
                    return "file", cand
            return "unresolved", spec
        pkg = "/".join(spec.split("/")[:2]) if spec.startswith("@") else spec.split("/")[0]
        if pkg in by_name:
            return "workspace", pkg
        return "external", ("node:" + pkg[5:] if pkg.startswith("node:") else pkg)

    imported_by = {p: set() for p in paths}
    ws_used_by = {name: set() for name in by_name}
    out = {}
    for r in files:
        d = dict(r)
        d["workspace"] = workspace_of(r["path"])
        d["package_name"] = packages.get(d["workspace"], {}).get("name", "")
        f_imp, w_imp, e_imp, bad = set(), set(), set(), set()
        for spec in r.get("import_specs", []):
            kind, target = resolve(r["path"], spec)
            {"file": f_imp, "workspace": w_imp, "external": e_imp, "unresolved": bad}[kind].add(target)
            if kind == "file":
                imported_by[target].add(r["path"])
            if kind == "workspace":
                ws_used_by[target].add(r["path"])
        d.update(imports_files=sorted(f_imp), imports_workspace=sorted(w_imp), imports_external=sorted(e_imp), imports_unresolved=sorted(bad))
        stem = re.sub(r"\.(test|spec)(\.[tj]sx?)$", r"\2", r["path"])
        if r["role"] == "test":
            d["tests_subject"] = stem if stem in paths and stem != r["path"] else ""
        out[r["path"]] = d
    for p, d in out.items():
        d["imported_by"] = sorted(imported_by[p])
        d["tested_by"] = sorted(t for t in paths if out[t].get("tests_subject") == p)

    # workspace packages
    pk = {}
    for d_, p in packages.items():
        deps = p.get("dependencies", {})
        ws_deps = sorted(n for n in deps if n in by_name)
        main = p.get("main")
        entry = posixpath.normpath(posixpath.join(d_, main)) if main else ""
        pk[d_] = {"dir": d_ or ".", "name": p.get("name", ""), "description": p.get("description", ""), "scripts": p.get("scripts", {}),
                  "workspace_deps": ws_deps, "external_deps": {n: v for n, v in sorted(deps.items()) if n not in by_name},
                  "entry": entry if entry in paths else "", "files": sum(1 for x in out.values() if x["workspace"] == d_),
                  "packageManager": p.get("packageManager"), "engines": p.get("engines")}
    name_to_dir = {v["name"]: k for k, v in pk.items()}
    for d_, v in pk.items():
        v["direct_dependents"] = sorted(o["name"] for o in pk.values() if v["name"] and v["name"] in o["workspace_deps"])
    for d_, v in pk.items():
        seen, stack = set(), list(v["direct_dependents"])
        while stack:
            n = stack.pop()
            if n not in seen:
                seen.add(n)
                stack.extend(pk[name_to_dir[n]]["direct_dependents"])
        v["all_dependents"] = sorted(seen)
        v["imported_from_files"] = len(ws_used_by.get(v["name"], ()))
    # entry points named by package scripts
    for d_, v in pk.items():
        for script, cmd in v["scripts"].items():
            for m in re.findall(r"(?:tsx|node|ts-node)\s+(?:watch\s+)?([\w./-]+\.[cm]?[tj]sx?)", cmd):
                target = posixpath.normpath(posixpath.join(d_, m))
                if target in out:
                    out[target].setdefault("run_by_scripts", []).append(f"{v['name'] or 'root'}: `{script}` = `{cmd}`")
        if v["entry"]:
            out[v["entry"]]["package_entry_of"] = v["name"]
    return out, pk


def md_list(items, empty="none"):
    return ", ".join(f"`{i}`" for i in items) if items else empty


def pages(manifest):
    """Second-brain pages from the manifest: one overview, one per workspace package, one per file."""
    files, pk = manifest["files"], manifest["packages"]
    out = []
    root = pk.get("", {})
    wfs = [f for f in files.values() if f.get("workflow")]
    dockerfiles = sorted(p for p in files if posixpath.basename(p) == "Dockerfile")
    deploy_words = re.compile(r"\b(deploy|publish|release|docker push|eas submit|eas build|render|fly deploy|kubectl|terraform apply)\b", re.I)
    deploying = [(f["path"], j["id"], r) for f in wfs for j in f["workflow"]["jobs"] for r in j["runs"] if deploy_words.search(r)]
    nvm = next((f.get("pin") for f in files.values() if f.get("pin")), None)
    eas = next((f.get("eas_profiles") for f in files.values() if f.get("eas_profiles")), None)
    migrations = sorted(f["path"] for f in files.values() if f["role"] == "database migration")
    L = [f"# Codebase overview: {manifest['repo_name']} at commit {manifest['commit'][:7]}", "",
         f"Tracked files: {len(files)}. Workspace packages: {len([d for d in pk if d])}. Generated deterministically from the code; no model wrote this page.", "",
         "## Toolchain",
         f"- Package manager pin: `{root.get('packageManager')}` (root `package.json`, field `packageManager`).",
         f"- Node.js: `.nvmrc` pins `{nvm}`; root `package.json` `engines` allows `{json.dumps(root.get('engines'))}`.", "",
         "## Root scripts (`package.json`)"]
    for s, c in (root.get("scripts") or {}).items():
        L.append(f"- `pnpm {s}` runs `{c}`")
    L += ["", "## Workspace packages and what depends on what", "", "| Package | Directory | Depends on (workspace) | Depended on by, directly | Depended on by, directly or through another package | Entry file |", "| --- | --- | --- | --- | --- | --- |"]
    for d_, v in sorted(pk.items()):
        if d_:
            L.append(f"| `{v['name']}` | `{d_}` | {md_list(v['workspace_deps'])} | {md_list(v['direct_dependents'])} | {md_list(v['all_dependents'])} | {('`' + v['entry'] + '`') if v['entry'] else 'none declared'} |")
    L += ["", "## Entry points and scripts that run a file"]
    for p, f in sorted(files.items()):
        bits = []
        if f.get("package_entry_of"):
            bits.append(f"`main` of `{f['package_entry_of']}`")
        bits += f.get("run_by_scripts", [])
        bits += f.get("marks", []) if (f.get("package_entry_of") or f.get("run_by_scripts")) or "starts a network listener" in f.get("marks", []) or "registers the mobile root component" in f.get("marks", []) else []
        if bits:
            L.append(f"- `{p}`: " + "; ".join(bits))
    L += ["", "## Continuous integration"]
    for f in sorted(wfs, key=lambda x: x["path"]):
        w = f["workflow"]
        L.append(f"- `{f['path']}` (workflow `{w['name']}`, triggers: {', '.join(w['triggers']) or 'not parsed'})")
        for j in w["jobs"]:
            L.append(f"  - job `{j['id']}`, named `{j['name']}`" + (f", service images {md_list(j['images'])}" if j["images"] else ""))
            for r in j["runs"]:
                L.append(f"    - `{r[:200]}`")
    L += ["", "## Deployment",
          ("- Workflow steps that deploy, publish or release: " + "; ".join(f"`{p}` job `{j}`: `{r[:120]}`" for p, j, r in deploying)) if deploying
          else "- No workflow step deploys, publishes or releases anything. The workflows above run checks only.",
          f"- Dockerfiles in the repository: {md_list(dockerfiles)}." + (" The only one is the development container; nothing builds an image of the API." if dockerfiles == [".devcontainer/Dockerfile"] else ""),
          f"- Mobile build profiles (`eas.json`): {md_list(eas or [])}." if eas else "- No mobile build profiles found.",
          "", "## Database migrations"]
    for m in migrations:
        t = files[m].get("tables_created", [])
        L.append(f"- `{m}`: {len(t)} CREATE TABLE statement(s)" + (f" ({', '.join(t)})" if t else "") + (f". {files[m]['purpose'][:160]}" if files[m].get("purpose") else ""))
    out.append({"path": "/", "kind": "code_overview", "title": f"Codebase overview: {manifest['repo_name']}", "body": "\n".join(L), "meta": {"commit": manifest["commit"]}})

    for d_, v in sorted(pk.items()):
        if not d_:
            continue
        L = [f"# Package `{v['name']}` ({d_}/)", "", v["description"] or "The package manifest has no description.", "",
             f"- Files: {v['files']}. Entry file: {('`' + v['entry'] + '`') if v['entry'] else 'none declared'}.",
             f"- Depends on workspace packages: {md_list(v['workspace_deps'])}.",
             f"- Depended on directly by: {md_list(v['direct_dependents'])}. Directly or through another package: {md_list(v['all_dependents'])}.",
             "- External dependencies: " + (", ".join(f"`{n}@{ver}`" for n, ver in v["external_deps"].items()) or "none") + ".", "", "## Scripts"]
        L += [f"- `{s}`: `{c}`" for s, c in v["scripts"].items()] or ["- none"]
        L += ["", "## Files"]
        for p, f in sorted(files.items()):
            if f["workspace"] == d_:
                L.append(f"- `{p}` ({f['role']})" + (f": {f['purpose'][:140]}" if f.get("purpose") else ""))
        out.append({"path": d_ + "/", "kind": "code_package", "title": f"Code package: {v['name']} ({d_})", "body": "\n".join(L), "meta": {"package": v["name"]}})

    for p, f in sorted(files.items()):
        L = [f"# `{p}`", "", f"- Role: {f['role']}." + (f" Package: `{f['package_name']}` (`{f['workspace']}/`)." if f.get("package_name") else ""),
             "- Purpose, in the file's own words: " + (f["purpose"] if f.get("purpose") else "the file has no leading comment or heading that says.")]
        if f.get("package_entry_of"):
            L.append(f"- Entry file (`main`) of `{f['package_entry_of']}`.")
        for s in f.get("run_by_scripts", []):
            L.append(f"- Run by package script {s}.")
        for m in f.get("marks", []):
            L.append(f"- It {m}.")
        if "import_specs" in f:
            L += [f"- Imports workspace packages: {md_list(f['imports_workspace'])}.", f"- Imports files: {md_list(f['imports_files'])}.",
                  f"- Imports external packages: {md_list(f['imports_external'])}.", f"- Imported by: {md_list(f['imported_by'])}.",
                  f"- Exports: {md_list(f.get('exports', [])[:40])}."]
            if f.get("imports_unresolved"):
                L.append(f"- Imports the mapper could not resolve: {md_list(f['imports_unresolved'])}.")
        if f["role"] == "test" and f.get("tests_subject"):
            L.append(f"- Tests `{f['tests_subject']}`.")
        if f.get("tested_by"):
            L.append(f"- Tested by: {md_list(f['tested_by'])}.")
        if f.get("tables_created") is not None and f["role"] == "database migration":
            L.append(f"- CREATE TABLE statements: {len(f['tables_created'])}" + (f" ({', '.join(f['tables_created'])})." if f["tables_created"] else "."))
        if f.get("package"):
            L.append("- Scripts: " + ("; ".join(f"`{s}` = `{c}`" for s, c in (f["package"].get("scripts") or {}).items()) or "none") + ".")
        if f.get("workflow"):
            L.append("- Jobs: " + "; ".join(f"`{j['id']}` (named `{j['name']}`)" for j in f["workflow"]["jobs"]) + ".")
        if f.get("env_keys"):
            L.append(f"- Environment variable names it lists: {md_list(f['env_keys'])}.")
        if f.get("images"):
            L.append(f"- Images: {md_list(f['images'])}.")
        if f.get("eas_profiles"):
            L.append(f"- Build profiles: {md_list(f['eas_profiles'])}.")
        L.append(f"- Size: {f.get('lines', '?')} lines, {f['bytes']} bytes. Blob `{f['sha'][:10]}`.")
        out.append({"path": p, "kind": "code_file", "title": f"Code: {p}", "body": "\n".join(L), "meta": {"role": f["role"], "blob": f["sha"]}})
    for pg in out:
        pg["content_sha"] = hashlib.sha256(pg["body"].encode()).hexdigest()
    return out


def build(repo, commit, old=None):
    tree = ls_tree(repo, commit)
    old_files = {f["path"]: f for f in (old or {}).get("raw", [])} if old and old.get("mapper_version") == MAPPER_VERSION else {}
    raw, reread = [], 0
    for path, sha in sorted(tree.items()):
        prev = old_files.get(path)
        if prev and prev["sha"] == sha:
            raw.append(prev)                    # unchanged blob: reuse, do not open the file
        else:
            raw.append(extract_file(repo, path, sha))
            reread += 1
    files, packages = derive(raw)
    repo_name = (packages.get("", {}).get("name") or posixpath.basename(repo.rstrip("/")))
    return {"mapper_version": MAPPER_VERSION, "repo_name": repo_name, "commit": git(repo, "rev-parse", commit).strip(),
            "stats": {"files": len(tree), "files_read": reread, "files_reused": len(tree) - reread,
                      "deleted": sorted(set(old_files) - set(tree)) if old_files else []},
            "raw": raw, "files": files, "packages": packages}


if __name__ == "__main__":
    mode, repo, commit = sys.argv[1], sys.argv[2], sys.argv[3]
    old = json.load(open(sys.argv[4])) if mode == "incr" else None
    m = build(repo, commit, old)
    json.dump(m, open(sys.argv[-1], "w"))
    unresolved = sum(len(f.get("imports_unresolved", [])) for f in m["files"].values())
    print(json.dumps({**m["stats"], "deleted": len(m["stats"]["deleted"]), "pages": len(pages(m)), "unresolved_relative_imports": unresolved, "commit": m["commit"][:7]}))
