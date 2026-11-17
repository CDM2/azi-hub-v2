"""R-02 spike, criterion 5: one model-driven agent doing one made-up coding task.

Two modes, the same loop, the same model, the same task statement:
  stack   run by Paperclip's `process` adapter. The team's conventions are a page in the organization's second
          brain, read through Paperclip's tool gateway from the permission service.
  plain   run directly as a single agent (the N-04 baseline). The same conventions are a file in the workspace.

Standard library only. Environment: TASK_MODE, TASK_DIR (workspace), TASK_OUT (result file), TASK_KEY_FILE,
TASK_STATEMENT (file), TASK_ISSUE_ID (stack only; optional), and, in stack mode, what Paperclip injects.
"""
import json, os, pathlib, subprocess, sys, time, urllib.error, urllib.request

MODE = os.environ.get("TASK_MODE", "plain")
WS = pathlib.Path(os.environ["TASK_DIR"]).resolve()
OUT = os.environ["TASK_OUT"]
MODEL = os.environ.get("TASK_MODEL", "claude-sonnet-5-5")
PRICE = {"in": 2.0, "out": 10.0, "cache_write": 2.5, "cache_read": 0.10}     # USD per million tokens (ledger E-77)
API = os.environ.get("PAPERCLIP_API_URL", "").rstrip("/")
MAX_TURNS, MAX_COST = 40, 3.0


def http(method, url, headers=None, body=None, timeout=120):
    req = urllib.request.Request(url, method=method, data=None if body is None else json.dumps(body).encode())
    req.add_header("Content-Type", "application/json")
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()
    except Exception as e:  # noqa: BLE001
        return 0, f"{type(e).__name__}: {e}"


class Gateway:
    """The organization's second brain, reached only through Paperclip's tool gateway."""

    def __init__(self):
        auth = {"Authorization": "Bearer " + os.environ.get("PAPERCLIP_API_KEY", "")}
        body = {"issueId": os.environ["TASK_ISSUE_ID"]} if os.environ.get("TASK_ISSUE_ID") else {}
        status, raw = http("POST", API + "/api/tool-gateway/sessions", auth, body)
        self.session_status = status
        self.token = json.loads(raw).get("token", "") if status in (200, 201) else ""
        self.names, self.calls = {}, []
        s2, r2 = http("GET", API + "/api/tool-gateway/tools", {"X-Paperclip-Tool-Gateway-Token": self.token})
        try:
            for d in json.loads(r2):
                self.names[d.get("upstreamToolName") or d.get("name")] = d.get("name")
        except (ValueError, TypeError, AttributeError):
            pass

    def call(self, tool, params):
        status, raw = http("POST", API + "/api/tool-gateway/tools/call", {"X-Paperclip-Tool-Gateway-Token": self.token},
                           {"tool": self.names.get(tool, tool), "parameters": params})
        self.calls.append({"tool": tool, "status": status})
        try:
            body = json.loads(raw)
        except ValueError:
            return f"gateway error {status}"
        if status == 200:
            return str((body.get("result") or {}).get("content"))[:12000]
        return f"refused ({status}): {body.get('error')}"


def safe(path):
    p = (WS / str(path).lstrip("/")).resolve()
    if p != WS and WS not in p.parents:
        raise ValueError("path is outside the workspace")
    return p


def tool_list_dir(a):
    p = safe(a.get("path", "."))
    return "\n".join(sorted(x.name + ("/" if x.is_dir() else "") for x in p.iterdir() if x.name not in ("__pycache__", ".git"))) if p.is_dir() else "no such directory"


def tool_read_file(a):
    p = safe(a["path"])
    return p.read_text()[:20000] if p.is_file() else "no such file"


def tool_write_file(a):
    p = safe(a["path"])
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(a["content"])
    return f"wrote {len(a['content'])} characters to {a['path']}"


def tool_run_tests(_a):
    r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-t", "."], cwd=WS, capture_output=True, text=True, timeout=120,
                       env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "PYTHONDONTWRITEBYTECODE": "1"})
    return (r.stdout + r.stderr)[-4000:]


def T(name, desc, props, required):
    return {"name": name, "description": desc, "input_schema": {"type": "object", "properties": props, "required": required}}


S = {"type": "string"}
TOOLS = [T("list_dir", "List a directory of the workspace.", {"path": S}, []),
         T("read_file", "Read a file in the workspace.", {"path": S}, ["path"]),
         T("write_file", "Create or replace a file in the workspace with the given full content.", {"path": S, "content": S}, ["path", "content"]),
         T("run_tests", "Run the repository's test suite and return its output.", {}, [])]
BRAIN_TOOLS = [T("brain_search", "Search your organization's second brain for pages (conventions, decisions, notes).", {"query": S}, ["query"]),
               T("brain_get", "Read one page of the second brain by id or by path.", {"id": S, "path": S}, [])]
SYSTEM = ("You are a careful software engineer working alone in a small repository. Do the task you are given, verify it by running the tests, "
          "and stop when it is done. Do not guess team conventions: look them up. ")
SYSTEM += ("Team conventions are kept in your organization's second brain; use brain_search and brain_get." if MODE == "stack"
           else "Team conventions are in the file docs/conventions.md in the workspace.")


def api(key, body):
    data = json.dumps(body).encode()
    for attempt in range(6):
        req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=data, method="POST",
                                     headers={"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            text = e.read().decode()[:300]
            if e.code in (429, 500, 502, 503, 529) and attempt < 5:
                time.sleep(min(60, 3 * 2 ** attempt)); continue
            raise RuntimeError(f"API {e.code}: {text}")
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt < 5:
                time.sleep(5 * (attempt + 1)); continue
            raise RuntimeError(f"API unreachable: {e}")


def main():
    t0 = time.time()
    res = {"mode": MODE, "model": MODEL, "turns": 0, "tool_calls": {}, "usage": {"input": 0, "output": 0, "cache_write": 0, "cache_read": 0}, "cost_usd": 0.0}
    key = pathlib.Path(os.environ["TASK_KEY_FILE"]).read_text().strip()
    gw = Gateway() if MODE == "stack" else None
    if gw:
        res["gateway_session_status"] = gw.session_status
        res["gateway_tools_seen"] = sorted(k for k in gw.names if k.startswith("brain_"))
    tools = TOOLS + (BRAIN_TOOLS if MODE == "stack" else [])
    handlers = {"list_dir": tool_list_dir, "read_file": tool_read_file, "write_file": tool_write_file, "run_tests": tool_run_tests}
    messages = [{"role": "user", "content": [{"type": "text", "text": pathlib.Path(os.environ["TASK_STATEMENT"]).read_text()}]}]
    system = [{"type": "text", "text": SYSTEM, "cache_control": {"type": "ephemeral"}}]
    final = ""
    while res["turns"] < MAX_TURNS and res["cost_usd"] < MAX_COST:
        res["turns"] += 1
        for m in messages:
            for b in m["content"]:
                b.pop("cache_control", None)
        messages[-1]["content"][-1]["cache_control"] = {"type": "ephemeral"}
        out = api(key, {"model": MODEL, "max_tokens": 4000, "system": system, "tools": tools, "messages": messages})
        u = out.get("usage", {})
        res["usage"]["input"] += u.get("input_tokens", 0); res["usage"]["output"] += u.get("output_tokens", 0)
        res["usage"]["cache_write"] += u.get("cache_creation_input_tokens", 0); res["usage"]["cache_read"] += u.get("cache_read_input_tokens", 0)
        res["cost_usd"] += (u.get("input_tokens", 0) * PRICE["in"] + u.get("output_tokens", 0) * PRICE["out"]
                            + u.get("cache_creation_input_tokens", 0) * PRICE["cache_write"] + u.get("cache_read_input_tokens", 0) * PRICE["cache_read"]) / 1e6
        content = out.get("content", [])
        messages.append({"role": "assistant", "content": content})
        final = "\n".join(b.get("text", "") for b in content if b.get("type") == "text")
        uses = [b for b in content if b.get("type") == "tool_use"]
        if out.get("stop_reason") != "tool_use" or not uses:
            break
        results = []
        for b in uses:
            name, a = b["name"], b.get("input") or {}
            res["tool_calls"][name] = res["tool_calls"].get(name, 0) + 1
            try:
                text = gw.call(name, a) if (gw and name.startswith("brain_")) else handlers[name](a)
            except Exception as e:  # noqa: BLE001
                text = f"tool error: {type(e).__name__}: {e}"
            results.append({"type": "tool_result", "tool_use_id": b["id"], "content": text})
        messages.append({"role": "user", "content": results})
    res.update(seconds=round(time.time() - t0, 1), cost_usd=round(res["cost_usd"], 4), final_message=final[:600],
               input_tokens_total=res["usage"]["input"] + res["usage"]["cache_write"] + res["usage"]["cache_read"],
               gateway_calls=gw.calls if gw else None, run_id=os.environ.get("PAPERCLIP_RUN_ID"))
    pathlib.Path(OUT).write_text(json.dumps(res, indent=1))
    print(f"task agent finished: mode {MODE}, {res['turns']} turns, ${res['cost_usd']}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # noqa: BLE001
        pathlib.Path(OUT).write_text(json.dumps({"mode": MODE, "fatal": f"{type(e).__name__}: {str(e)[:400]}"}))
        print("task agent failed:", e)
        sys.exit(1)
