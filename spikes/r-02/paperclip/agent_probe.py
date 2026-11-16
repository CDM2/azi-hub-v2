"""The scripted agent. Paperclip's built-in `process` adapter runs this as an agent's heartbeat.

It does what a model-driven agent's harness would do, with no model: take the run's own
credentials from the environment Paperclip injects, open a tool-gateway session, and call the
permission service's tools through Paperclip's MCP gateway. It never talks to the service directly.
Standard library only.
"""
import hashlib, json, os, sys, time, urllib.error, urllib.request

API = os.environ.get("PAPERCLIP_API_URL", "").rstrip("/")
KEY = os.environ.get("PAPERCLIP_API_KEY", "")
_plan = json.load(open(os.environ["PROBE_PLAN"]))
PLAN = _plan["steps"] if isinstance(_plan, dict) else _plan
ISSUE_ID = _plan.get("issue_id") if isinstance(_plan, dict) else None
RUNNER_CREDENTIALS = {"GH_TOKEN", "GITHUB_TOKEN", "SPIKE_MODEL_KEY", "ANTHROPIC_API_KEY", "ACTIONS_RUNTIME_TOKEN", "ACTIONS_ID_TOKEN_REQUEST_TOKEN"}
OUT = os.environ["PROBE_OUT"]


def http(method, url, headers=None, body=None):
    req = urllib.request.Request(url, method=method, data=None if body is None else json.dumps(body).encode())
    req.add_header("Content-Type", "application/json")
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()
    except Exception as e:  # noqa: BLE001
        return 0, f"{type(e).__name__}: {e}"


def main():
    out = {"started": time.time(), "steps": [],
           "env": sorted(k for k in os.environ if k.startswith("PAPERCLIP_")),
           "env_names_other": sorted(k for k in os.environ if not k.startswith("PAPERCLIP_")),
           # the scratch machine's own credentials, by name, plus anything the CI runner sets for its jobs
           "leaked_env": sorted(k for k in os.environ if k in RUNNER_CREDENTIALS or k.startswith(("ACTIONS_", "RUNNER_")) or k in ("GITHUB_REPOSITORY", "GITHUB_RUN_ID", "GITHUB_WORKSPACE")),
           "user": os.environ.get("USER"), "uid": os.getuid()}
    out["run_id"] = os.environ.get("PAPERCLIP_RUN_ID")
    out["has_run_token"] = bool(KEY)
    if os.environ.get("PROBE_SECRET"):
        out["secret_sha256"] = hashlib.sha256(os.environ["PROBE_SECRET"].encode()).hexdigest()
    if os.environ.get("PROBE_ECHO") and os.environ.get("PROBE_SECRET"):
        print("secret-echo: " + os.environ["PROBE_SECRET"])          # on purpose: does the run log redact it?
    if os.environ.get("PROBE_SLEEP"):
        with open(OUT + ".started", "w") as f:
            f.write(str(os.getpid()))
        time.sleep(float(os.environ["PROBE_SLEEP"]))
    auth = {"Authorization": "Bearer " + KEY} if KEY else {}
    status, raw = http("GET", API + "/api/agents/me", auth)
    out["me"] = {"status": status, "body": raw[:600]}
    if os.environ.get("PROBE_FOREIGN_COMPANY"):
        own = os.environ.get("PAPERCLIP_COMPANY_ID")
        out["boundary"] = {"own_company_agents": http("GET", f"{API}/api/companies/{own}/agents", auth)[0],
                           "other_company_agents": http("GET", f"{API}/api/companies/{os.environ['PROBE_FOREIGN_COMPANY']}/agents", auth)[0],
                           "other_company_gateway_audit": http("GET", f"{API}/api/tool-gateway/audit?companyId={os.environ['PROBE_FOREIGN_COMPANY']}", auth)[0]}
    ids = {} if KEY else {"companyId": os.environ.get("PAPERCLIP_COMPANY_ID"), "agentId": os.environ.get("PAPERCLIP_AGENT_ID"), "runId": os.environ.get("PAPERCLIP_RUN_ID")}
    if ISSUE_ID:
        ids["issueId"] = ISSUE_ID          # approvals are posted on a task, so an ask-first call needs a task-scoped session
    status, raw = http("POST", API + "/api/tool-gateway/sessions", auth, ids)
    out["session"] = {"status": status, "body": raw[:200] if status != 200 and status != 201 else "ok"}
    token, names = "", {}
    try:
        sess = json.loads(raw)
        token = sess.get("token", "")
        out["session"]["keys"] = sorted(sess.keys())
        if sess.get("toolsUrl"):
            s2, r2 = http("GET", sess["toolsUrl"] if sess["toolsUrl"].startswith("http") else API + sess["toolsUrl"], {"X-Paperclip-Tool-Gateway-Token": token})
            out["tools"] = {"status": s2, "body": r2[:6000]}
            try:
                for d in json.loads(r2):
                    names[d.get("upstreamToolName") or d.get("name")] = d.get("name")
            except (ValueError, AttributeError, TypeError):
                pass
    except ValueError:
        pass
    out["tool_names"] = names
    gw = {"X-Paperclip-Tool-Gateway-Token": token}
    for step in PLAN:
        # The gateway gives each tool its own name; a tool the agent was not shown is called by its plain name.
        body = {"tool": names.get(step["tool"], step["tool"]), "parameters": step.get("parameters", {})}
        t0 = time.time()
        status, raw = http("POST", API + "/api/tool-gateway/tools/call", gw, body)
        rec = {"label": step.get("label"), "tool": step["tool"], "gateway_tool": body["tool"], "parameters": step.get("parameters", {}), "status": status,
               "ms": round((time.time() - t0) * 1000), "raw": raw[:20000]}
        if status == 409 and step.get("wait_for_approval"):
            # An ask-first tool. Paperclip has posted an approval card on the task; wait for the human's decision.
            try:
                ar = json.loads(raw).get("actionRequestId")
            except ValueError:
                ar = None
            rec["action_request_id"] = ar
            with open(OUT + ".waiting.tmp", "w") as f:
                f.write(json.dumps({"action_request_id": ar, "label": step.get("label")}))
            os.replace(OUT + ".waiting.tmp", OUT + ".waiting")
            deadline = time.time() + 120
            while time.time() < deadline and not os.path.exists(OUT + ".approved"):
                time.sleep(0.5)
            if os.path.exists(OUT + ".approved"):
                try:
                    rec["decision_seen"] = json.load(open(OUT + ".approved"))
                except ValueError:
                    rec["decision_seen"] = None
                os.remove(OUT + ".approved")
            # What does a retry of the identical call do after the decision? Recorded as evidence only.
            s3, r3 = http("POST", API + "/api/tool-gateway/tools/call", gw, dict(body, approvedActionRequestId=ar))
            rec["retry"] = {"status": s3, "raw": r3[:4000]}
        out["steps"].append(rec)
    out["finished"] = time.time()
    with open(OUT, "w") as f:
        json.dump(out, f)
    print(f"probe finished: {len(out['steps'])} steps")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # noqa: BLE001
        with open(OUT, "w") as f:
            json.dump({"fatal": f"{type(e).__name__}: {e}"}, f)
        print("probe failed", e)
        sys.exit(1)
