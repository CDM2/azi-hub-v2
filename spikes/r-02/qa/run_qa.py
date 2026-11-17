"""R-02 spike, criterion 8: score three agents on the 20 questions.

  (a) map only            the agent reads Toveli's codebase pages in the second brain and nothing else
  (b) map, then raw code  the same pages first, then read-only access to the code
  (c) plain agent         one agent with read-only access to the code and no map (the N-04 baseline)

All three are the same minimal tool loop on the same model; only the tools differ. Standard library only.
Code is read through git at one commit, so nothing in the repository is touched. Transcripts stay outside
this repository (they quote Toveli source); only scores, token counts and the one-line answers are kept.

  run_qa.py <repo> <commit> <out.json> [--runs 2] [--arms a,b,c] [--only Q01,Q02] [--workers 4]
Environment: ANTHROPIC_KEY_FILE, BRAIN_SOCKET, QA_TRANSCRIPTS (directory), SPEND_FILE, SPEND_CAP (default 95).
"""
import concurrent.futures as cf, fnmatch, json, os, pathlib, re, subprocess, sys, threading, time, urllib.error, urllib.request

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parent / "mapper"))
import grade                      # noqa: E402
from brainclient import Brain     # noqa: E402

MODEL = os.environ.get("QA_MODEL", "claude-sonnet-5-5")
PRICE = {"in": 2.0, "out": 10.0, "cache_write": 2.5, "cache_read": 0.10}   # USD per million tokens, Sonnet 5.5 list (ledger E-77)
KEY = pathlib.Path(os.environ.get("ANTHROPIC_KEY_FILE", "/root/.spike/anthropic.key")).read_text().strip()
SPEND_FILE = pathlib.Path(os.environ.get("SPEND_FILE", "/root/.spike/spend.json"))
SPEND_CAP = float(os.environ.get("SPEND_CAP", "95"))
TRANSCRIPTS = pathlib.Path(os.environ.get("QA_TRANSCRIPTS", "/home/claude/work/qa"))
FIXTURE = json.loads((HERE.parent / "tests" / "fixture.json").read_text())
TOVELI_TOKEN = next(p["token"] for p in FIXTURE["principals"] if p["org"] == "toveli" and p["actor"] == "agent")
MAX_TURNS, LOCK = 24, threading.Lock()


class BudgetStop(Exception):
    pass


def spend(add=0.0, label="qa"):
    with LOCK:
        s = json.loads(SPEND_FILE.read_text()) if SPEND_FILE.exists() else {"total": 0.0, "by": {}}
        if add:
            s["total"] = round(s["total"] + add, 6)
            s["by"][label] = round(s["by"].get(label, 0.0) + add, 6)
            SPEND_FILE.write_text(json.dumps(s))
        return s["total"]


def api(body):
    if spend() >= SPEND_CAP:
        raise BudgetStop(f"spend cap reached: ${spend():.2f}")
    data = json.dumps(body).encode()
    for attempt in range(7):
        req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=data, method="POST",
                                     headers={"x-api-key": KEY, "anthropic-version": "2023-06-01", "content-type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                out = json.loads(r.read())
            u = out.get("usage", {})
            cost = (u.get("input_tokens", 0) * PRICE["in"] + u.get("output_tokens", 0) * PRICE["out"]
                    + u.get("cache_creation_input_tokens", 0) * PRICE["cache_write"] + u.get("cache_read_input_tokens", 0) * PRICE["cache_read"]) / 1e6
            spend(cost, body.get("metadata", {}).get("user_id", "qa"))
            out["_cost"] = cost
            return out
        except urllib.error.HTTPError as e:
            text = e.read().decode()[:300]
            if e.code in (429, 500, 502, 503, 529) and attempt < 6:
                time.sleep(min(60, 3 * 2 ** attempt))
                continue
            raise RuntimeError(f"API {e.code}: {text}")
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt < 6:
                time.sleep(5 * (attempt + 1))
                continue
            raise RuntimeError(f"API unreachable: {e}")


# ------------------------------------------------------------------------------------------- tools

class Repo:
    def __init__(self, path, commit):
        self.path, self.commit = path, commit
        out = subprocess.run(["git", "-C", path, "ls-tree", "-r", "--name-only", commit], capture_output=True, text=True, check=True).stdout
        self.files = sorted(out.splitlines())

    def list_dir(self, path=""):
        path = path.strip("/")
        prefix = path + "/" if path else ""
        names = sorted({f[len(prefix):].split("/")[0] + ("/" if "/" in f[len(prefix):] else "") for f in self.files if f.startswith(prefix)})
        return "\n".join(names) if names else f"no such directory: {path}"

    def glob(self, pattern):
        hits = [f for f in self.files if fnmatch.fnmatch(f, pattern)]
        return "\n".join(hits[:200]) if hits else "no files match"

    def grep(self, pattern, path_prefix="", max_results=40):
        args = ["git", "-C", self.path, "grep", "-n", "-I", "-E", "-e", pattern, self.commit]
        if path_prefix:
            args += ["--", path_prefix.strip("/")]
        out = subprocess.run(args, capture_output=True, text=True).stdout
        lines = [l.split(":", 1)[1][:260] for l in out.splitlines() if ":" in l]
        more = f"\n... {len(lines) - max_results} more matches" if len(lines) > max_results else ""
        return ("\n".join(lines[:max_results]) + more) if lines else "no matches"

    def read_file(self, path, start_line=1, max_lines=200):
        path = path.strip("/")
        if path not in self.files:
            return f"no such file: {path}"
        raw = subprocess.run(["git", "-C", self.path, "show", f"{self.commit}:{path}"], capture_output=True).stdout
        if b"\0" in raw[:2000]:
            return "binary file"
        lines = raw.decode("utf-8", "replace").splitlines()
        start = max(1, int(start_line)); n = max(1, min(400, int(max_lines)))
        chunk = lines[start - 1:start - 1 + n]
        tail = f"\n... file has {len(lines)} lines; showing {start}-{start - 1 + len(chunk)}" if len(lines) > start - 1 + len(chunk) else ""
        return "\n".join(f"{start + i}: {l[:300]}" for i, l in enumerate(chunk))[:24000] + tail


class Map:
    def __init__(self):
        self.brain = Brain()

    def _fmt(self, ok, payload, body=False):
        if not ok:
            return "not found in the map"
        if body:
            return payload["page"]["body"][:24000]
        return "\n".join(f"{p['path']}  [{p['kind']}]" + (f"  {re.sub(chr(10), ' ', p.get('snippet', ''))[:160]}" if p.get("snippet") else "") for p in payload["pages"]) or "nothing in the map matches"

    def overview(self):
        return self._fmt(*self.brain.tool(TOVELI_TOKEN, "brain_get", {"path": "/"}), body=True)

    def get(self, path):
        ok, payload = self.brain.tool(TOVELI_TOKEN, "brain_get", {"path": path})
        if not ok and not path.endswith("/"):
            ok, payload = self.brain.tool(TOVELI_TOKEN, "brain_get", {"path": path.rstrip("/") + "/"})
        return self._fmt(ok, payload, body=True)

    def search(self, query):
        return self._fmt(*self.brain.tool(TOVELI_TOKEN, "brain_search", {"query": query, "source_type": "codebase", "limit": 25}))

    def list(self, prefix=""):
        ok, payload = self.brain.tool(TOVELI_TOKEN, "brain_list", {"source_type": "codebase", "limit": 200})
        if ok:
            payload["pages"] = [p for p in payload["pages"] if p["path"].startswith(prefix.lstrip("/"))][:200]
            for p in payload["pages"]:
                p.pop("snippet", None)
        return self._fmt(ok, payload)


def tool(name, desc, props, required):
    return {"name": name, "description": desc, "input_schema": {"type": "object", "properties": props, "required": required}}


S = {"type": "string"}; I = {"type": "integer"}
MAP_TOOLS = [
    tool("map_overview", "The codebase map's overview page: toolchain, root scripts, packages and their dependencies, entry points, CI, deployment, migrations.", {}, []),
    tool("map_get", "One page of the codebase map: a file's page (path like apps/api/src/main.ts) or a package's page (path like apps/api/).", {"path": S}, ["path"]),
    tool("map_search", "Search the codebase map's pages (titles, purposes, imports, exports) for a word or phrase.", {"query": S}, ["query"]),
    tool("map_list", "List the map's pages under a path prefix.", {"prefix": S}, []),
]
CODE_TOOLS = [
    tool("list_dir", "List a directory of the repository.", {"path": S}, []),
    tool("glob", "List files matching a glob pattern, for example packages/db/**/*.sql or *.json.", {"pattern": S}, ["pattern"]),
    tool("grep", "Search file contents with an extended regular expression. Optional path prefix.", {"pattern": S, "path_prefix": S}, ["pattern"]),
    tool("read_file", "Read a file with line numbers. Up to 400 lines per call.", {"path": S, "start_line": I, "max_lines": I}, ["path"]),
]
COMMON = ("You answer one question about a software repository. Work it out with the tools; do not guess. "
          "If the tools you have cannot settle the question, say what you could not determine. "
          "End your reply with exactly one line that starts with 'ANSWER:' and holds the answer in at most 300 characters. "
          "When the question asks for a list of names, the ANSWER line is a comma-separated list of the short names and nothing else.")
ARMS = {
    "a": {"name": "map only", "tools": MAP_TOOLS,
          "system": COMMON + " You have a codebase map kept in the organization's second brain: an overview page, one page per package and one per file. You cannot read the code itself."},
    "b": {"name": "map, then raw code", "tools": MAP_TOOLS + CODE_TOOLS,
          "system": COMMON + " You have a codebase map kept in the organization's second brain, and read-only access to the code. Consult the map first. Open the code only when the map does not settle the question."},
    "c": {"name": "plain agent, no map", "tools": CODE_TOOLS,
          "system": COMMON + " You have read-only access to the repository: list directories, glob, grep and read files."},
}


def run_tool(repo, mp, name, a):
    try:
        if name == "map_overview": return mp.overview()
        if name == "map_get": return mp.get(str(a.get("path", "")))
        if name == "map_search": return mp.search(str(a.get("query", "")))
        if name == "map_list": return mp.list(str(a.get("prefix", "")))
        if name == "list_dir": return repo.list_dir(str(a.get("path", "")))
        if name == "glob": return repo.glob(str(a.get("pattern", "")))
        if name == "grep": return repo.grep(str(a.get("pattern", "")), str(a.get("path_prefix", "")))
        if name == "read_file": return repo.read_file(str(a.get("path", "")), a.get("start_line", 1), a.get("max_lines", 200))
    except Exception as e:  # noqa: BLE001
        return f"tool error: {type(e).__name__}: {e}"
    return "unknown tool"


def ask(repo, arm, q, run_no):
    cfg, mp = ARMS[arm], Map()
    messages = [{"role": "user", "content": [{"type": "text", "text": q["question"]}]}]
    usage = {"input": 0, "cache_write": 0, "cache_read": 0, "output": 0}
    cost, turns, calls, t0, final, tools_used = 0.0, 0, 0, time.time(), "", []
    system = [{"type": "text", "text": cfg["system"], "cache_control": {"type": "ephemeral"}}]
    while turns < MAX_TURNS:
        turns += 1
        for m in messages:                                   # keep one moving cache breakpoint on the newest block
            for b in m["content"]:
                b.pop("cache_control", None)
        messages[-1]["content"][-1]["cache_control"] = {"type": "ephemeral"}
        out = api({"model": MODEL, "max_tokens": 1500, "system": system, "tools": cfg["tools"], "messages": messages,
                   "metadata": {"user_id": f"qa-arm-{arm}"}})
        u = out.get("usage", {})
        usage["input"] += u.get("input_tokens", 0); usage["output"] += u.get("output_tokens", 0)
        usage["cache_write"] += u.get("cache_creation_input_tokens", 0); usage["cache_read"] += u.get("cache_read_input_tokens", 0)
        cost += out["_cost"]
        content = out.get("content", [])
        messages.append({"role": "assistant", "content": content})
        uses = [b for b in content if b.get("type") == "tool_use"]
        final = "\n".join(b.get("text", "") for b in content if b.get("type") == "text")
        if out.get("stop_reason") != "tool_use" or not uses:
            break
        results = []
        for b in uses:
            calls += 1; tools_used.append(b["name"])
            results.append({"type": "tool_result", "tool_use_id": b["id"], "content": run_tool(repo, mp, b["name"], b.get("input") or {})})
        messages.append({"role": "user", "content": results})
    score, correct, detail = grade.grade(q["id"], final)
    TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
    (TRANSCRIPTS / f"{arm}-run{run_no}-{q['id']}.json").write_text(json.dumps(messages))
    return {"arm": arm, "run": run_no, "id": q["id"], "category": q["category"], "correct": correct, "score": round(score, 3), "detail": detail,
            "answer": grade.answer_line(final)[:300], "turns": turns, "tool_calls": calls,
            "tools_used": {t: tools_used.count(t) for t in sorted(set(tools_used))},
            "input_tokens": usage["input"] + usage["cache_write"] + usage["cache_read"], "output_tokens": usage["output"],
            "usage": usage, "cost_usd": round(cost, 5), "seconds": round(time.time() - t0, 1), "model": out.get("model")}


def summarize(rows):
    out = {}
    for arm in sorted({r["arm"] for r in rows}):
        rs = [r for r in rows if r["arm"] == arm and "error" not in r]
        if not rs:
            continue
        n = len(rs)
        per_run = {}
        for r in rs:
            per_run.setdefault(r["run"], []).append(r["correct"])
        cats = {}
        for r in rs:
            c = cats.setdefault(r["category"], [0, 0]); c[0] += r["correct"]; c[1] += 1
        out[arm] = {"name": ARMS[arm]["name"], "answers": n, "correct": sum(r["correct"] for r in rs), "accuracy": round(sum(r["correct"] for r in rs) / n, 3),
                    "correct_per_run": {k: f"{sum(v)}/{len(v)}" for k, v in sorted(per_run.items())},
                    "mean_input_tokens": round(sum(r["input_tokens"] for r in rs) / n), "mean_output_tokens": round(sum(r["output_tokens"] for r in rs) / n),
                    "mean_seconds": round(sum(r["seconds"] for r in rs) / n, 1), "mean_tool_calls": round(sum(r["tool_calls"] for r in rs) / n, 1),
                    "mean_cost_usd": round(sum(r["cost_usd"] for r in rs) / n, 4), "total_cost_usd": round(sum(r["cost_usd"] for r in rs), 3),
                    "by_category": {k: f"{v[0]}/{v[1]}" for k, v in sorted(cats.items())}}
    return out


def main():
    repo_path, commit, out_path = sys.argv[1], sys.argv[2], pathlib.Path(sys.argv[3])
    opt = dict(zip(sys.argv[4::2], sys.argv[5::2]))
    runs, arms, workers = int(opt.get("--runs", 2)), opt.get("--arms", "a,b,c").split(","), int(opt.get("--workers", 4))
    only = set(opt["--only"].split(",")) if "--only" in opt else None
    repo = Repo(repo_path, commit)
    qs = [q for q in grade.QUESTIONS.values() if not only or q["id"] in only]
    jobs = [(arm, q, r) for r in range(1, runs + 1) for arm in arms for q in qs]
    rows, start_spend = [], spend()
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(ask, repo, arm, q, r): (arm, q["id"], r) for arm, q, r in jobs}
        for f in cf.as_completed(futs):
            arm, qid, r = futs[f]
            try:
                rows.append(f.result())
            except Exception as e:  # noqa: BLE001
                rows.append({"arm": arm, "run": r, "id": qid, "error": f"{type(e).__name__}: {str(e)[:200]}"})
    rows.sort(key=lambda x: (x["arm"], x["run"], x["id"]))
    report = {"model": MODEL, "commit": commit, "runs_per_arm": runs, "questions": len(qs), "max_turns": MAX_TURNS,
              "prices_usd_per_million": PRICE, "spend_this_run_usd": round(spend() - start_spend, 3), "spend_total_usd": round(spend(), 3),
              "errors": [r for r in rows if "error" in r], "summary": summarize(rows), "rows": [r for r in rows if "error" not in r]}
    out_path.write_text(json.dumps(report, indent=1))
    print(json.dumps({"spend_this_run": report["spend_this_run_usd"], "errors": len(report["errors"]), "summary": report["summary"]}, indent=1))


if __name__ == "__main__":
    main()
