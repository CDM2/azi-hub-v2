"""R-02 spike: drive an unmodified Paperclip and check criteria 1 to 4 through its MCP gateway.

Runs on the scratch machine as the runner user. Standard library only. Paperclip runs in
local_trusted mode, where local requests are the board operator (Paperclip docs/api/authentication.md).

Usage: harness.py <phase> <out_dir>      phases: setup | checks | governance
State (company and agent IDs) is kept in <work>/state.json so a later phase, or the same checks
after an upgrade, reuse what an earlier phase created.
"""
import json, os, pathlib, re, sys, time, urllib.error, urllib.request, uuid

PC = os.environ.get("PAPERCLIP_URL", "http://127.0.0.1:3100")
BRAIN = os.environ.get("BRAIN_URL", "http://127.0.0.1:8900")
BRAIN_ADMIN = os.environ["BRAIN_ADMIN_TOKEN"]
WORK = pathlib.Path(os.environ.get("SPIKE_WORK", "/srv/pcwork"))
HERE = pathlib.Path(__file__).resolve().parent
FIXTURE = json.loads((HERE.parent / "tests" / "fixture.json").read_text())
TOKENS = {p["org"]: p["token"] for p in FIXTURE["principals"] if p["actor"] == "agent"}
ORGS = ["mgmt", "toveli", "sibling", "personal"]
STATE = WORK / "state.json"
TRACE = []


def http(method, url, body=None, headers=None, timeout=120):
    req = urllib.request.Request(url, method=method, data=None if body is None else json.dumps(body).encode())
    req.add_header("Content-Type", "application/json")
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            status, raw = r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        status, raw = e.code, e.read().decode()
    except Exception as e:  # noqa: BLE001
        status, raw = 0, f"{type(e).__name__}: {e}"
    try:
        data = json.loads(raw) if raw else None
    except ValueError:
        data = None
    TRACE.append({"m": method, "url": url.replace(PC, "PC").replace(BRAIN, "BRAIN"), "status": status,
                  "req": redact(body), "res": redact(data) if data is not None else raw[:400]})
    return status, data, raw


def redact(obj, depth=0):
    """Keep traces small and free of tokens."""
    if isinstance(obj, dict):
        return {k: ("<redacted>" if re.search(r"token|secret|authorization|credential", k, re.I) and isinstance(v, (str, dict)) else redact(v, depth + 1))
                for k, v in list(obj.items())[:40]}
    if isinstance(obj, list):
        return [redact(v, depth + 1) for v in obj[:6]] + ([f"... {len(obj) - 6} more"] if len(obj) > 6 else [])
    if isinstance(obj, str) and len(obj) > 300:
        return obj[:300] + "..."
    return obj


def pc(method, path, body=None):
    return http(method, PC + path, body)


def brain_admin(method, path, body=None):
    status, data, raw = http(method, BRAIN + path, body, {"Authorization": "Bearer " + BRAIN_ADMIN})
    assert status == 200, f"brain admin {path}: {status} {raw[:200]}"
    return data


def load_state():
    return json.loads(STATE.read_text()) if STATE.exists() else {"orgs": {}}


def save_state(st):
    STATE.write_text(json.dumps(st, indent=1))


# ---------------------------------------------------------------------------------------------- setup

def agent_config(org, extra_env=None):
    plan, outp = WORK / f"plan-{org}.json", WORK / f"out-{org}.json"
    if not plan.exists():
        plan.write_text("[]")
    env = {"PROBE_PLAN": str(plan), "PROBE_OUT": str(outp)}
    env.update(extra_env or {})
    return {"command": "python3", "args": [str(WORK / "agent_probe.py")], "cwd": str(WORK), "timeoutSec": 300, "graceSec": 5, "env": env}


def ensure_company(st, org, token, ask_first=("brain_write",), hidden=("publish_briefing",)):
    """A Paperclip company with one scripted agent and the permission service connected with that organization's token."""
    o = st["orgs"].setdefault(org, {})
    if "company_id" not in o:
        status, data, raw = pc("POST", "/api/companies", {"name": f"spike-{org}", "description": f"R-02 spike organization {org} (made-up data)"})
        assert status in (200, 201), f"create company {org}: {status} {raw[:300]}"
        o["company_id"] = data["id"]
    cid = o["company_id"]
    if "agent_id" not in o:
        body = {"name": f"{org}-probe", "role": "engineer", "title": "Scripted probe agent",
                "capabilities": "Calls the permission service through the tool gateway",
                "adapterType": "process", "adapterConfig": agent_config(org)}
        status, data, raw = pc("POST", f"/api/companies/{cid}/agents", body)
        assert status in (200, 201), f"create agent {org}: {status} {raw[:400]}"
        o["agent_id"] = data.get("id") or data.get("agent", {}).get("id")
        o["agent_status"] = data.get("status") or data.get("agent", {}).get("status")
    if "connection_id" not in o:
        body = {"link": BRAIN + "/mcp", "name": "Permission service", "authMode": "bearer",
                "credentialValues": {"credentials.authorization": token}}
        status, data, raw = pc("POST", f"/api/companies/{cid}/tools/apps/connect", body)
        assert status in (200, 201), f"connect {org}: {status} {raw[:600]}"
        o["connection_id"] = data.get("connectionId") or data.get("connection", {}).get("id")
        o["connect_keys"] = sorted(data.keys())
        o["catalog"] = {e.get("toolName"): {"id": e.get("id"), "risk": e.get("riskLevel"), "status": e.get("status"), "readOnly": e.get("isReadOnly")}
                        for e in (data.get("catalog") or [])}
        save_state(st)
    if not o.get("finished"):
        cat = o["catalog"]
        asks = [cat[n]["id"] for n in ask_first if n in cat and (org == "toveli" or n != "brain_write")]
        if org == "personal" and "publish_briefing" in cat:
            asks.append(cat["publish_briefing"]["id"])
        enabled = [v["id"] for k, v in cat.items() if (k not in hidden or org == "personal") and v["id"] not in asks]
        status, data, raw = pc("POST", f"/api/companies/{cid}/tools/apps/{o['connection_id']}/finish",
                               {"enabledCatalogEntryIds": enabled, "askFirstCatalogEntryIds": asks, "access": "all_agents"})
        assert status == 200, f"finish {org}: {status} {raw[:600]}"
        o["finished"] = True
        o["finish_keys"] = sorted((data or {}).keys())
    status, data, _ = pc("GET", f"/api/companies/{cid}/tools/profiles/effective/agents/{o['agent_id']}")
    o["allowed_tools"] = (data or {}).get("allowedToolNames")
    save_state(st)
    return o


def setup(out):
    st = load_state()
    status, health, _ = pc("GET", "/api/health")
    st["paperclip_health"] = health
    brain_admin("POST", "/admin/reset", FIXTURE)
    for org in ORGS:
        ensure_company(st, org, TOKENS[org])
    return st


# ---------------------------------------------------------------------------------------------- runs

def rid():
    return str(uuid.uuid4())


def run_agent(st, org, plan, approve=None, timeout=150):
    """Give the scripted agent a plan, trigger one heartbeat, wait for its output file."""
    o = st["orgs"][org]
    plan_path, out_path = WORK / f"plan-{org}.json", WORK / f"out-{org}.json"
    for p in (out_path, pathlib.Path(str(out_path) + ".waiting"), pathlib.Path(str(out_path) + ".approved")):
        if p.exists():
            p.unlink()
    for step in plan:
        step.setdefault("parameters", {})["request_id"] = rid()
    plan_path.write_text(json.dumps(plan))
    status, data, raw = pc("POST", f"/api/agents/{o['agent_id']}/heartbeat/invoke", {})
    invoke = {"status": status, "body": redact(data) if data else raw[:300]}
    deadline = time.time() + timeout
    waiting = pathlib.Path(str(out_path) + ".waiting")
    approvals = []
    while time.time() < deadline and not out_path.exists():
        if waiting.exists() and approve:
            info = json.loads(waiting.read_text())
            waiting.unlink()
            approvals.append(approve(o, info))
            pathlib.Path(str(out_path) + ".approved").write_text("ok")
        time.sleep(1)
    result = json.loads(out_path.read_text()) if out_path.exists() else {"fatal": "no output file: the agent run did not complete"}
    result["invoke"] = invoke
    result["approvals"] = approvals
    result["plan"] = plan
    status, runs, _ = pc("GET", f"/api/companies/{o['company_id']}/heartbeat-runs?agentId={o['agent_id']}&limit=5")
    result["runs"] = redact(runs)
    return result


def gateway_audit(company_id, max_pages=12):
    """All of one company's gateway audit events (the API pages 100 at a time)."""
    events, cursor, status = [], None, 0
    for _ in range(max_pages):
        status, data, raw = pc("GET", f"/api/tool-gateway/audit?companyId={company_id}&limit=100" + (f"&cursor={cursor}" if cursor else ""))
        if status != 200 or not isinstance(data, dict):
            return status, events, raw[:300]
        events += data.get("events") or []
        cursor = data.get("nextCursor")
        if not cursor:
            break
    return status, events, ""


def approve_action(o, info):
    status, data, raw = pc("POST", f"/api/tool-gateway/action-requests/{info['action_request_id']}/approve", {"companyId": o["company_id"]})
    return {"status": status, "body": redact(data) if data else raw[:300]}


def step_text(result, label=None):
    """Everything an agent received for one step (or all steps), as one string to search for markers."""
    steps = [s for s in result.get("steps", []) if label is None or s.get("label") == label]
    return "\n".join(s.get("raw", "") + json.dumps(s.get("retry", "")) for s in steps)


MARK = lambda org: re.compile(r"CANARY-%s" % org, re.I)


def check(results, name, ok, detail=""):
    results.append({"check": name, "pass": bool(ok), "detail": str(detail)[:400]})


def checks(out):
    st = load_state()
    brain_admin("POST", "/admin/reset", FIXTURE)
    res, runs = [], {}
    audit_start = max([r["id"] for r in brain_admin("GET", "/admin/audit?since_id=0")["rows"]] or [0])

    # sibling first, so its page IDs can be used against it
    runs["sibling"] = run_agent(st, "sibling", [
        {"label": "whoami", "tool": "brain_whoami"},
        {"label": "search-all", "tool": "brain_search", "parameters": {"query": "CANARY", "limit": 100}},
        {"label": "list-code", "tool": "brain_list", "parameters": {"source_type": "codebase"}},
        {"label": "get-toveli-code", "tool": "brain_get", "parameters": {"path": "apps/example/main.ts"}},
    ])
    if "fatal" in runs["sibling"] or not runs["sibling"].get("steps"):
        (out / "checks.json").write_text(json.dumps({"summary": {"passed": 0, "failed": 1, "aborted": "the first agent run did not complete; nothing else was attempted"},
                                                      "runs": {"sibling": redact_run(runs["sibling"])}}, indent=1))
        print("ABORT: first agent run did not complete:", json.dumps(redact_run(runs["sibling"]))[:1500])
        return False
    sib_ids = re.findall(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", step_text(runs["sibling"], "search-all"))
    sibling_page = sib_ids[0] if sib_ids else str(uuid.uuid4())

    runs["toveli"] = run_agent(st, "toveli", [
        {"label": "whoami", "tool": "brain_whoami"},
        {"label": "list", "tool": "brain_list", "parameters": {"limit": 100}},
        {"label": "search-all", "tool": "brain_search", "parameters": {"query": "CANARY", "limit": 100}},
        {"label": "search-sibling-marker", "tool": "brain_search", "parameters": {"query": "CANARY-SIBLING-1"}},
        {"label": "search-sibling-words", "tool": "brain_search", "parameters": {"query": "confidential roadmap"}},
        {"label": "get-sibling-id", "tool": "brain_get", "parameters": {"id": sibling_page}},
        {"label": "get-missing-id", "tool": "brain_get", "parameters": {"id": str(uuid.uuid4())}},
        {"label": "get-sibling-path", "tool": "brain_get", "parameters": {"path": "services/quant/run.py"}},
        {"label": "list-as-sibling", "tool": "brain_list", "parameters": {"org": "sibling", "org_id": "sibling"}},
        {"label": "search-as-personal", "tool": "brain_search", "parameters": {"query": "CANARY", "org": "personal"}},
        {"label": "search-personal-words", "tool": "brain_search", "parameters": {"query": "goals for the year"}},
        {"label": "write-health", "tool": "brain_write", "parameters": {"title": "s", "body": "CANARY-SENSITIVE-GW", "sensitivity": "health"}, "wait_for_approval": True},
        {"label": "write-note", "tool": "brain_write", "parameters": {"title": "gw note", "body": "CANARY-TOVELI-GW written through the gateway"}, "wait_for_approval": True},
        {"label": "briefing-from-org", "tool": "publish_briefing", "parameters": {"content": "CANARY-BRIEFING-FORGED"}},
        {"label": "unknown-tool", "tool": "brain_admin_dump", "parameters": {}},
    ], approve=approve_action)

    runs["personal"] = run_agent(st, "personal", [
        {"label": "whoami", "tool": "brain_whoami"},
        {"label": "search-all", "tool": "brain_search", "parameters": {"query": "CANARY", "limit": 100}},
        {"label": "briefing", "tool": "publish_briefing", "parameters": {"content": "CANARY-BRIEFING-GW priorities, published through the gateway."}, "wait_for_approval": True},
    ], approve=approve_action)

    runs["mgmt-before"] = run_agent(st, "mgmt", [
        {"label": "whoami", "tool": "brain_whoami"},
        {"label": "search-all", "tool": "brain_search", "parameters": {"query": "CANARY", "limit": 100}},
        {"label": "search-briefing", "tool": "brain_search", "parameters": {"query": "CANARY-BRIEFING-GW"}},
    ])
    briefing_id = None
    m = re.search(r'briefing_id\\?"\s*:\s*\\?"([0-9a-f-]{36})', step_text(runs["personal"], "briefing"))
    if m:
        briefing_id = m.group(1)
        brain_admin("POST", "/admin/approve_briefing", {"briefing_id": briefing_id, "approver": "founder (spike harness)"})
    runs["mgmt-after"] = run_agent(st, "mgmt", [
        {"label": "search-briefing", "tool": "brain_search", "parameters": {"query": "CANARY-BRIEFING-GW"}},
    ])
    runs["toveli-after"] = run_agent(st, "toveli", [
        {"label": "search-briefing", "tool": "brain_search", "parameters": {"query": "CANARY-BRIEFING-GW"}},
        {"label": "search-own-write", "tool": "brain_search", "parameters": {"query": "CANARY-TOVELI-GW"}},
    ])

    for name, r in runs.items():
        check(res, f"run completed: {name}", "fatal" not in r and len(r.get("steps", [])) == len(r["plan"]), r.get("fatal") or r.get("invoke"))
        check(res, f"agent process got no runner credential in its environment: {name}", not r.get("leaked_env"), r.get("leaked_env"))

    t, s, mg, p = runs["toveli"], runs["sibling"], runs["mgmt-before"], runs["personal"]
    # Criterion 1
    all_t = step_text(t) + step_text(runs["toveli-after"])
    check(res, "C1 toveli agent identified as toveli by the service", '"toveli' in step_text(t, "whoami").replace("\\", ""), step_text(t, "whoami")[:200])
    check(res, "C1 toveli agent sees its own and global pages", all(x in step_text(t, "search-all") for x in ["CANARY-TOVELI-1", "CANARY-TOVELI-2", "CANARY-TOVELI-3", "CANARY-GLOBAL-1"]))
    for org in ["SIBLING", "PERSONAL", "MGMT"]:
        check(res, f"C1 no {org} page ever reached the toveli agent (any step, any run)", not MARK(org).search(all_t), MARK(org).findall(all_t)[:3])
    gs, gm = [x for x in t.get("steps", []) if x["label"] == "get-sibling-id"], [x for x in t.get("steps", []) if x["label"] == "get-missing-id"]
    same = bool(gs and gm) and gs[0]["status"] == gm[0]["status"] and re.sub(r"[0-9a-f-]{36}", "ID", gs[0]["raw"]) == re.sub(r"[0-9a-f-]{36}", "ID", gm[0]["raw"])
    check(res, "C1 a sibling's page looks exactly like a missing page", same, (gs[0]["raw"][:150] if gs else "") + " | " + (gm[0]["raw"][:150] if gm else ""))
    check(res, "C1 sibling agent sees its own pages", "CANARY-SIBLING-1" in step_text(s, "search-all"))
    check(res, "C1 no toveli page (codebase pages included) reached the sibling agent", not MARK("TOVELI").search(step_text(s)), MARK("TOVELI").findall(step_text(s))[:3])
    check(res, "C1 no personal or holding-only page reached the sibling agent", not MARK("PERSONAL").search(step_text(s)) and not MARK("MGMT").search(step_text(s)))
    # Criterion 2
    check(res, "C2 holding agent reads both sub-organizations", all(x in step_text(mg, "search-all") for x in ["CANARY-TOVELI-1", "CANARY-TOVELI-3", "CANARY-SIBLING-1", "CANARY-MGMT-1", "CANARY-GLOBAL-1"]))
    check(res, "C2 no personal page reached the holding agent", not MARK("PERSONAL").search(step_text(mg) + step_text(runs["mgmt-after"])))
    # Criterion 3
    check(res, "C3 personal agent reads its organizations", all(x in step_text(p, "search-all") for x in ["CANARY-PERSONAL-1", "CANARY-TOVELI-1", "CANARY-SIBLING-1", "CANARY-MGMT-1"]))
    check(res, "C3 an organization's agent cannot publish a briefing", "CANARY-BRIEFING-FORGED" not in step_text(runs["mgmt-after"]) and "pending" not in step_text(t, "briefing-from-org"), step_text(t, "briefing-from-org")[:200])
    check(res, "C3 a health page is refused outside personal, even after Paperclip's approval", '"id"' not in step_text(t, "write-health").replace("\\", "") or "forbidden" in step_text(t, "write-health"), step_text(t, "write-health")[:300])
    check(res, "C3 briefing accepted from the personal agent as pending", briefing_id is not None, step_text(p, "briefing")[:300])
    check(res, "C3 briefing invisible to the holding agent before the human approves it", "CANARY-BRIEFING-GW" not in step_text(mg, "search-briefing"))
    check(res, "C3 briefing visible to the holding agent after approval", "CANARY-BRIEFING-GW" in step_text(runs["mgmt-after"], "search-briefing"))
    check(res, "C3 briefing never reaches a sub-organization", "CANARY-BRIEFING-GW" not in step_text(runs["toveli-after"]))
    check(res, "ask-first tool: the write waited for Paperclip approval and then landed", "CANARY-TOVELI-GW" in step_text(runs["toveli-after"], "search-own-write"), json.dumps(t.get("approvals"))[:300])

    # Criterion 4: both audit logs
    brain_rows = brain_admin("GET", f"/admin/audit?since_id={audit_start}")["rows"]
    brain_by_rid = {}
    for r in brain_rows:
        if r.get("request_id"):
            brain_by_rid.setdefault(r["request_id"], []).append(r)
    pc_events, pc_raw = {}, {}
    for org in ORGS:
        status, events, err = gateway_audit(st["orgs"][org]["company_id"])
        pc_events[org] = events
        pc_raw[org] = {"status": status, "count": len(events), "error": err, "sample": redact(events[:2]),
                       "actions": sorted({str(e.get("action")) for e in events}), "outcomes": sorted({str(e.get("normalizedOutcome")) for e in events})}
    made, in_brain, pc_only, how, unmatched = 0, 0, 0, {"invocation id": 0, "action request id": 0, "request id in the logged arguments": 0, "run, tool and order": 0}, []
    for name, r in runs.items():
        org = name.split("-")[0]
        events = pc_events.get(org, [])
        used = set()
        for stp in r.get("steps", []):
            made += 1
            request_id = stp["parameters"]["request_id"]
            try:
                body = json.loads(stp["raw"])
            except ValueError:
                body = {}
            body = body if isinstance(body, dict) else {}
            inv, areq = body.get("invocationId"), stp.get("action_request_id") or body.get("actionRequestId")
            match = None
            for e in events:
                d = e.get("details") or {}
                if inv and d.get("invocationId") == inv:
                    match = ("invocation id", e); break
                if areq and d.get("actionRequestId") == areq:
                    match = ("action request id", e); break
                if request_id in json.dumps(e):
                    match = ("request id in the logged arguments", e); break
            if not match:   # a call Paperclip stopped before it created an invocation: same run, same tool, not used yet
                for e in sorted(events, key=lambda x: x.get("createdAt") or ""):
                    d = e.get("details") or {}
                    if e.get("id") not in used and e.get("runId") == r.get("run_id") and d.get("toolName") in (stp.get("gateway_tool"), stp["tool"]):
                        match = ("run, tool and order", e); break
            b = brain_by_rid.get(request_id, [])
            in_brain += bool(b)
            pc_only += (not b)
            if match:
                how[match[0]] += 1
                used.add(match[1].get("id"))
            else:
                unmatched.append({"run": name, "label": stp["label"], "status": stp["status"], "invocation": inv, "raw": stp["raw"][:160]})
    in_pc = sum(how.values())
    check(res, "C4 every gateway call is in Paperclip's audit log", made > 0 and in_pc == made, f"calls {made}; matched by {how}; unmatched {unmatched[:4]}")
    check(res, "C4 every call that reached the service is in the service's audit log with the same request ID", in_brain > 0 and in_brain + pc_only == made,
          f"calls {made}, in service audit {in_brain}, never reached the service (stopped by Paperclip) {pc_only}")
    by_org = {}
    for r_ in brain_rows:
        by_org.setdefault(r_.get("org") or "none", {}).setdefault(r_["decision"], 0)
        by_org[r_.get("org") or "none"][r_["decision"]] += 1
    denied = [r for r in brain_rows if r["decision"] == "deny"]
    check(res, "C4 the service logged its own denials", len(denied) >= 3, f"{len(denied)} denied rows")
    # a call around Paperclip: straight to the service with the organization's token
    direct_rid = rid()
    http("POST", BRAIN + "/mcp", {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "brain_list", "arguments": {"request_id": direct_rid}}},
         {"Authorization": "Bearer " + TOKENS["toveli"]})
    after = brain_admin("GET", f"/admin/audit?since_id={audit_start}")["rows"]
    status, events, _ = gateway_audit(st["orgs"]["toveli"]["company_id"])
    check(res, "C4 limit recorded: a call that goes around Paperclip is in the service's log only",
          any(r.get("request_id") == direct_rid for r in after) and direct_rid not in json.dumps(events), "this is a known limit (ledger E-89), not a pass of criterion 4")

    summary = {"passed": sum(c["pass"] for c in res), "failed": sum(not c["pass"] for c in res), "calls_made_through_gateway": made,
               "in_paperclip_audit": in_pc, "paperclip_audit_matched_by": how, "in_service_audit": in_brain, "stopped_by_paperclip_first": pc_only,
               "service_audit_by_org": by_org, "paperclip_version": (pc("GET", "/api/health")[1] or {}).get("version")}
    (out / "checks.json").write_text(json.dumps({"summary": summary, "checks": res, "paperclip_audit": pc_raw,
                                                  "service_audit_rows": brain_rows[:80], "runs": {k: redact_run(v) for k, v in runs.items()}}, indent=1))
    print(json.dumps(summary))
    for c in res:
        print(("PASS " if c["pass"] else "FAIL ") + c["check"] + ("" if c["pass"] else "  <- " + c["detail"]))
    return summary["failed"] == 0


def redact_run(r):
    keep = {k: v for k, v in r.items() if k in ("env", "leaked_env", "me", "session", "invoke", "approvals", "fatal", "runs", "run_id", "has_run_token", "tool_names", "secret_sha256")}
    keep["tools"] = (r.get("tools") or {}).get("body", "")[:1500]
    keep["steps"] = [{"label": s["label"], "tool": s["tool"], "gateway_tool": s.get("gateway_tool"), "status": s["status"], "ms": s.get("ms"), "raw": s["raw"][:700],
                      "retry": (s.get("retry") or {}).get("raw", "")[:300] if s.get("retry") else None} for s in r.get("steps", [])]
    return keep


if __name__ == "__main__":
    phase, out = sys.argv[1], pathlib.Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    ok = True
    try:
        if phase == "setup":
            st = setup(out)
            (out / "setup.json").write_text(json.dumps(redact(st), indent=1))
        elif phase == "checks":
            ok = checks(out)
        elif phase == "governance":
            import governance
            ok = governance.run(out, sys.modules[__name__])
    except Exception as e:  # noqa: BLE001
        import traceback
        ok = False
        (out / f"{phase}-error.txt").write_text(traceback.format_exc())
        print("ERROR", type(e).__name__, str(e)[:500])
    finally:
        (out / f"{phase}-trace.json").write_text(json.dumps(TRACE[-400:], indent=1))
    sys.exit(0 if ok else 1)
