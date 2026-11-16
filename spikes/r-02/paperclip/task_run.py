"""R-02 spike, criterion 5 on the scratch machine: one model-driven task through Paperclip and the permission
service, and the same task on one plain agent (the N-04 baseline). Needs a model key in SPIKE_MODEL_KEY; without
one it records "not run" and stops. Made-up repository and conventions only.

  task_run.py <out_dir>
"""
import json, os, pathlib, re, shutil, subprocess, sys, time, uuid

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import harness as h   # noqa: E402

OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
KEY = os.environ.get("SPIKE_MODEL_KEY", "").strip()
WORK, KEYFILE = h.WORK, h.WORK / ".model-key"
PCENV = ["sudo", "-u", "pclip", "-H", "env", "-i", "PATH=/opt/node24/bin:/usr/local/bin:/usr/bin:/bin", "HOME=/home/pclip", "USER=pclip", "LANG=C.UTF-8"]


def save(obj):
    (OUT / "task.json").write_text(json.dumps(obj, indent=1))


def workspace(name, with_conventions):
    ws = WORK / f"task-{name}"
    subprocess.run(["sudo", "rm", "-rf", str(ws)], check=False)
    shutil.copytree(HERE / "task" / "repo", ws, ignore=shutil.ignore_patterns("__pycache__"))
    if with_conventions:
        (ws / "docs").mkdir()
        shutil.copy(HERE / "task" / "conventions.md", ws / "docs" / "conventions.md")
    subprocess.run(["sudo", "chown", "-R", "pclip:pclip", str(ws)], check=True)
    return ws


def outcome(ws):
    subprocess.run(["sudo", "chmod", "-R", "a+rX", str(ws)], check=False)
    r = subprocess.run([sys.executable, str(HERE / "task" / "hidden" / "test_hidden.py"), str(ws)], capture_output=True, text=True, timeout=120,
                       env={"PATH": os.environ["PATH"], "PYTHONDONTWRITEBYTECODE": "1"})
    text = r.stdout + r.stderr
    ran = re.search(r"Ran (\d+) tests", text)
    bad = re.search(r"FAILED \((.*?)\)", text)
    return {"hidden_tests_ran": int(ran.group(1)) if ran else 0, "passed_all": r.returncode == 0, "failures": bad.group(1) if bad else None,
            "failed_names": re.findall(r"^(?:FAIL|ERROR): (\w+)", text, re.M)}


def main():
    if not KEY:
        save({"status": "not run", "reason": "no model key on the scratch machine (repository secret SPIKE_MODEL_KEY is not set)"})
        print("criterion 5: not run, no model key")
        return 0
    st = h.load_state()
    o = st["orgs"]["toveli"]
    cid = o["company_id"]
    result = {"status": "run", "model": "claude-sonnet-5-5", "arms": {}}
    subprocess.run(["sudo", "install", "-o", "pclip", "-g", "pclip", "-m", "600", "/dev/stdin", str(KEYFILE)], input=KEY, text=True, check=True)
    try:
        shutil.copy(HERE / "task" / "TASK.md", WORK / "TASK.md")
        # the conventions live in the organization's second brain, written by a human of that organization
        human = next(p["token"] for p in h.FIXTURE["principals"] if p["org"] == "toveli" and p["actor"] == "human")
        status, data, raw = h.http("POST", h.BRAIN + "/mcp", {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "brain_write", "arguments": {
            "title": "Pricing conventions", "body": (HERE / "task" / "conventions.md").read_text(), "request_id": str(uuid.uuid4())}}},
            {"Authorization": "Bearer " + human})
        result["conventions_page_written"] = status == 200 and "isError\": true" not in raw and '"isError":true' not in raw
        repeats = int(os.environ.get("TASK_REPEATS", "3"))
        result["repeats"] = repeats
        result["runs"] = []
        for i in range(1, repeats + 1):
            pair = {}
            audit_before = max([r["id"] for r in h.brain_admin("GET", "/admin/audit?since_id=0")["rows"]] or [0])

            # stack arm: an agent inside Paperclip
            ws = workspace(f"stack-{i}", with_conventions=False)
            out_stack = WORK / f"task-stack-result-{i}.json"
            subprocess.run(["sudo", "rm", "-f", str(out_stack)], check=False)
            env = {"TASK_MODE": "stack", "TASK_DIR": str(ws), "TASK_OUT": str(out_stack), "TASK_KEY_FILE": str(KEYFILE), "TASK_STATEMENT": str(WORK / "TASK.md")}
            if o.get("issue_id"):
                env["TASK_ISSUE_ID"] = o["issue_id"]
            status, agent, raw = h.pc("POST", f"/api/companies/{cid}/agents", {
                "name": f"toveli-task-agent-{i}", "role": "engineer", "title": "Model-driven task agent (criterion 5)", "adapterType": "process",
                "adapterConfig": {"command": "python3", "args": [str(WORK / "task_agent.py")], "cwd": str(ws), "timeoutSec": 900, "graceSec": 5, "env": env}})
            assert status in (200, 201), f"create task agent: {status} {raw[:300]}"
            t0 = time.time()
            si, di, rawi = h.pc("POST", f"/api/agents/{agent['id']}/heartbeat/invoke", {})
            while time.time() - t0 < 900 and not out_stack.exists():
                time.sleep(2)
            time.sleep(1)
            arm = json.loads(out_stack.read_text()) if out_stack.exists() else {"fatal": f"no result after {round(time.time() - t0)} s; invoke {si} {rawi[:200]}"}
            arm["wall_seconds_including_paperclip"] = round(time.time() - t0, 1)
            arm["outcome"] = outcome(ws)
            rows = [r for r in h.brain_admin("GET", f"/admin/audit?since_id={audit_before}")["rows"] if r.get("org") == "toveli"]
            arm["service_audit_rows"] = {"allow": sum(r["decision"] == "allow" for r in rows), "deny": sum(r["decision"] == "deny" for r in rows), "tools": sorted({r["tool"] for r in rows})}
            s_, events, _ = h.gateway_audit(cid)
            mine = [e for e in events if e.get("runId") == arm.get("run_id")]
            arm["paperclip_audit_events_for_the_run"] = len(mine)
            arm["paperclip_audit_tools"] = sorted({str((e.get("details") or {}).get("toolName")).split(":")[-1] for e in mine})
            pair["stack"] = arm

            # plain arm: one agent, no Paperclip, no permission service
            ws2 = workspace(f"plain-{i}", with_conventions=True)
            out_plain = WORK / f"task-plain-result-{i}.json"
            subprocess.run(["sudo", "rm", "-f", str(out_plain)], check=False)
            t0 = time.time()
            subprocess.run(PCENV + ["TASK_MODE=plain", f"TASK_DIR={ws2}", f"TASK_OUT={out_plain}", f"TASK_KEY_FILE={KEYFILE}", f"TASK_STATEMENT={WORK / 'TASK.md'}",
                                    "python3", str(WORK / "task_agent.py")], cwd=str(WORK), timeout=900, capture_output=True)
            arm = json.loads(out_plain.read_text()) if out_plain.exists() else {"fatal": "no result"}
            arm["wall_seconds_including_paperclip"] = round(time.time() - t0, 1)
            arm["outcome"] = outcome(ws2)
            pair["plain"] = arm
            result["runs"].append(pair)
            if i == 1:
                result["arms"] = pair
            result["spend_usd"] = round(sum((a.get("cost_usd") or 0) for pr in result["runs"] for a in pr.values()), 4)
            save(result)

        def mean(arm_name, key):
            vals = [pr[arm_name].get(key) for pr in result["runs"] if isinstance(pr[arm_name].get(key), (int, float))]
            return round(sum(vals) / len(vals), 4) if vals else None
        result["summary"] = {a: {"runs": len(result["runs"]), "passed_all": sum(bool(pr[a].get("outcome", {}).get("passed_all")) for pr in result["runs"]),
                                 "mean_cost_usd": mean(a, "cost_usd"), "mean_seconds": mean(a, "seconds"), "mean_turns": mean(a, "turns"),
                                 "mean_input_tokens": mean(a, "input_tokens_total"), "mean_wall_seconds": mean(a, "wall_seconds_including_paperclip")} for a in ("stack", "plain")}
    finally:
        subprocess.run(["sudo", "rm", "-f", str(KEYFILE)], check=False)
        save(result)
    print(json.dumps(result.get("summary")))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # noqa: BLE001
        import traceback
        (OUT / "task-error.txt").write_text(traceback.format_exc())
        print("criterion 5 error:", type(e).__name__, str(e)[:300])
        sys.exit(1)
