"""R-02 spike, criterion 7: exercise the governance controls of an unmodified, free-edition Paperclip.

Each probe does something through Paperclip's own API and records what happened. A control counts as
"works in the free edition" only if the probe saw it take effect; anything else is recorded as it was seen.
Runs in its own Paperclip company ("gov") so nothing here changes the companies criteria 1 to 4 use.
"""
import datetime, hashlib, json, os, pathlib, time

SECRET_VALUE = "spike-secret-" + hashlib.sha256(b"r-02 made-up secret").hexdigest()[:24]   # made-up, not a credential


def run(out, h):
    st = h.load_state()
    G = os.environ.get("GOV_KEY", "gov")            # one fresh Paperclip company per pass, so a pass never inherits state
    o = h.ensure_company(st, G, h.TOKENS["sibling"], ask_first=())
    cid, aid = o["company_id"], o["agent_id"]
    known = {}                                      # gateway tool names the agent saw while everything was allowed
    other = st["orgs"]["toveli"]["company_id"]
    probes = []

    def record(control, probe, observed, verdict):
        probes.append({"control": control, "probe": probe, "observed": observed, "verdict": verdict})
        print(f"{verdict.upper():28} {control}: {probe}")

    def guarded(fn):
        try:
            fn()
        except Exception as e:  # noqa: BLE001
            record(fn.__doc__ or fn.__name__, "probe raised an error", f"{type(e).__name__}: {str(e)[:300]}", "not verified")

    def set_env(extra):
        s, d, raw = h.pc("PATCH", f"/api/agents/{aid}", {"adapterConfig": h.agent_config(G, extra)})
        return s, raw[:300]

    def baseline():
        """Baseline: the agent runs and reaches its tools"""
        r = h.run_agent(st, G, [{"label": "whoami", "tool": "brain_whoami"}, {"label": "list", "tool": "brain_list"}], timeout=120)
        ok = "fatal" not in r and all(s["status"] == 200 for s in r.get("steps", []))
        known.update(r.get("tool_names") or {})
        record("baseline", "scripted agent runs one heartbeat and calls two tools through the gateway",
               {"statuses": [s["status"] for s in r.get("steps", [])], "has_run_token": r.get("has_run_token"), "fatal": r.get("fatal")}, "works" if ok else "failed")

    def tool_policy():
        """Tool and MCP policy: block rule"""
        s, pol, raw = h.pc("POST", f"/api/companies/{cid}/tools/policies",
                           {"name": "spike: block brain_list", "policyType": "block", "priority": 10, "selectors": {"toolName": "brain_list"}})
        r = h.run_agent(st, G, [{"label": "blocked", "tool": "brain_list"},
                                {"label": "blocked-by-known-name", "tool": known.get("brain_list", "brain_list")},
                                {"label": "still-allowed", "tool": "brain_whoami"}], timeout=120)
        steps = {x["label"]: x for x in r.get("steps", [])}
        listed = "brain_list" in (r.get("tool_names") or {})
        by_name = steps.get("blocked-by-known-name", {})
        blocked = (not listed) and by_name.get("status") in (403, 404) and steps.get("blocked", {}).get("status") not in (200, None)
        allowed = steps.get("still-allowed", {}).get("status") == 200
        if s in (200, 201) and pol and pol.get("id"):
            h.pc("DELETE", f"/api/companies/{cid}/tools/policies/{pol['id']}")
        r2 = h.run_agent(st, G, [{"label": "after-delete", "tool": "brain_list"}], timeout=120)
        restored = [x["status"] for x in r2.get("steps", [])] == [200]
        record("tool and MCP policy", "a block rule on one tool, for one company; then the rule is deleted",
               {"policy_create_status": s, "policy_create_body": raw[:160], "tool_still_listed_to_the_agent": listed,
                "call_by_plain_name": {"status": steps.get("blocked", {}).get("status"), "raw": (steps.get("blocked", {}).get("raw") or "")[:160]},
                "call_by_the_gateway_name_it_knew": {"status": by_name.get("status"), "raw": (by_name.get("raw") or "")[:260]},
                "other_tool_status": steps.get("still-allowed", {}).get("status"), "after_delete_status": [x["status"] for x in r2.get("steps", [])]},
               "works in the free edition" if (s in (200, 201) and blocked and allowed and restored) else "not verified")

    def pause_and_kill():
        """Pause or kill"""
        s1, d1, raw1 = h.pc("POST", f"/api/agents/{aid}/pause", {})
        r = h.run_agent(st, G, [{"label": "while-paused", "tool": "brain_whoami"}], timeout=25)
        ran_while_paused = "fatal" not in r
        s2, d2, raw2 = h.pc("POST", f"/api/agents/{aid}/resume", {})
        r2 = h.run_agent(st, G, [{"label": "after-resume", "tool": "brain_whoami"}], timeout=120)
        record("pause", "pause the agent, trigger a heartbeat, resume, trigger again",
               {"pause_status": s1, "agent_status_after_pause": (d1 or {}).get("status"), "invoke_while_paused": r.get("invoke"), "ran_while_paused": ran_while_paused,
                "resume_status": s2, "ran_after_resume": "fatal" not in r2},
               "works in the free edition" if (s1 == 200 and not ran_while_paused and "fatal" not in r2) else "not verified")
        # kill a run that is in flight
        set_env({"PROBE_SLEEP": "90"})
        started = pathlib.Path(str(h.WORK / f"out-{G}.json") + ".started")
        if started.exists():
            started.unlink()
        (h.WORK / f"plan-{G}.json").write_text('{"steps": []}')
        outp = h.WORK / f"out-{G}.json"
        if outp.exists():
            outp.unlink()
        si, di, rawi = h.pc("POST", f"/api/agents/{aid}/heartbeat/invoke", {})
        t0 = time.time()
        while time.time() - t0 < 60 and not started.exists():
            time.sleep(1)
        pid = int(started.read_text()) if started.exists() else None
        s, runs, _ = h.pc("GET", f"/api/companies/{cid}/heartbeat-runs?agentId={aid}&limit=5")
        running = [x for x in (runs or []) if isinstance(x, dict) and x.get("status") in ("running", "queued")]
        run_id = (running[0]["id"] if running else (di or {}).get("id"))
        sc, dc, rawc = h.pc("POST", f"/api/heartbeat-runs/{run_id}/cancel", {}) if run_id else (0, None, "no running run found")
        alive = None
        for _ in range(30):
            time.sleep(1)
            try:
                os.kill(pid, 0); alive = True
            except ProcessLookupError:
                alive = False; break
            except PermissionError:
                alive = True
            except TypeError:
                break
        sr, dr, _ = h.pc("GET", f"/api/heartbeat-runs/{run_id}") if run_id else (0, None, "")
        set_env({})
        record("kill", "cancel a heartbeat run while the agent's process is still working",
               {"process_started": pid is not None, "cancel_status": sc, "cancel_body": (rawc or "")[:200], "process_alive_after_cancel": alive,
                "seconds_to_stop": round(time.time() - t0, 1), "run_status_after": (dr or {}).get("status"), "run_error_code": (dr or {}).get("errorCode"),
                "agent_finished_its_work": outp.exists()},
               "works in the free edition" if (sc in (200, 201, 202) and alive is False and not outp.exists()) else "not verified")

    def secrets():
        """Secrets"""
        s, sec, raw = h.pc("POST", f"/api/companies/{cid}/secrets", {"name": "spike-probe-secret", "value": SECRET_VALUE, "description": "made-up value for the R-02 spike"})
        sid = (sec or {}).get("id")
        create_leaks = SECRET_VALUE in raw
        sp, rawp = set_env({"PROBE_SECRET": {"type": "secret_ref", "secretId": sid}, "PROBE_ECHO": "1"}) if sid else (0, "no secret id")
        sg, ag, rawg = h.pc("GET", f"/api/agents/{aid}")
        r = h.run_agent(st, G, [{"label": "whoami", "tool": "brain_whoami"}], timeout=120)
        got = r.get("secret_sha256") == hashlib.sha256(SECRET_VALUE.encode()).hexdigest()
        run_id = r.get("run_id")
        time.sleep(3)
        sl, dl, rawl = h.pc("GET", f"/api/heartbeat-runs/{run_id}/log") if run_id else (0, None, "")
        se, de, rawe = h.pc("GET", f"/api/heartbeat-runs/{run_id}/events") if run_id else (0, None, "")
        sx, dx, rawx = h.pc("GET", f"/api/heartbeat-runs/{run_id}") if run_id else (0, None, "")
        log_has_echo_line = "secret-echo" in (rawl + rawe + rawx)
        log_leaks = SECRET_VALUE in (rawl + rawe + rawx)
        set_env({})
        record("secrets", "store a secret, bind it to the agent's environment by reference, run the agent, have the agent print it, read the run log",
               {"create_status": s, "create_response_contains_value": create_leaks, "bind_status": sp, "bind_body": rawp[:200] if sp != 200 else "ok",
                "agent_config_read_contains_value": SECRET_VALUE in rawg, "agent_process_received_value": got, "run_log_status": sl,
                "run_log_has_the_echo_line": log_has_echo_line, "run_log_contains_value": log_leaks,
                "value_found_in": [n for n, body in (("run log", rawl), ("run events", rawe), ("run record", rawx)) if SECRET_VALUE in body], "fatal": r.get("fatal")},
               "works in the free edition" if (s in (200, 201) and got and not create_leaks and SECRET_VALUE not in rawg and log_has_echo_line and not log_leaks)
               else ("partly works" if (s in (200, 201) and got and SECRET_VALUE not in rawg) else "not verified"))

    def boundary():
        """Company boundary"""
        set_env({"PROBE_FOREIGN_COMPANY": other})
        r = h.run_agent(st, G, [{"label": "whoami", "tool": "brain_whoami"}], timeout=120)
        set_env({})
        b = r.get("boundary") or {}
        record("company boundary", "an agent uses its own run token to read its own company, another company's agents and another company's gateway audit",
               {**b, "has_run_token": r.get("has_run_token")},
               "works in the free edition" if (r.get("has_run_token") and b.get("own_company_agents") == 200 and b.get("other_company_agents") in (401, 403, 404)
                                                 and b.get("other_company_gateway_audit") in (401, 403, 404)) else "not verified")

    def spend_cap():
        """Spend caps"""
        B = G + "-budget"
        sa, da, rawa = h.pc("POST", f"/api/companies/{cid}/agents", {"name": f"{B}-probe", "role": "general", "adapterType": "process", "adapterConfig": h.agent_config(B)})
        aid = (da or {}).get("id")                 # shadows the outer agent on purpose
        st["orgs"][B] = {"company_id": cid, "agent_id": aid, "issue_id": o.get("issue_id")}
        r0 = h.run_agent(st, B, [], timeout=90)
        s1, d1, raw1 = h.pc("PATCH", f"/api/agents/{aid}/budgets", {"budgetMonthlyCents": 100})
        now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        s2, d2, raw2 = h.pc("POST", f"/api/companies/{cid}/cost-events",
                            {"agentId": aid, "provider": "spike", "model": "none", "costCents": 150, "occurredAt": now, "billingType": "unknown"})
        time.sleep(2)
        s3, a3, _ = h.pc("GET", f"/api/agents/{aid}")
        r = h.run_agent(st, B, [], timeout=25)
        s4, ov, raw4 = h.pc("GET", f"/api/companies/{cid}/budgets/overview")
        blocked = "fatal" in r
        s5, _, raw5 = h.pc("PATCH", f"/api/agents/{aid}/budgets", {"budgetMonthlyCents": 100000})
        s6, _, raw6 = h.pc("POST", f"/api/agents/{aid}/resume", {})
        r2 = h.run_agent(st, B, [], timeout=40)
        record("spend caps", "a second agent runs once; set a $1.00 monthly budget on it, report $1.50 of cost, trigger a heartbeat, raise the budget, trigger again",
               {"ran_before_the_budget": "fatal" not in r0, "set_budget_status": s1, "cost_event_status": s2, "cost_event_body": raw2[:200] if s2 not in (200, 201) else "ok",
                "agent_status_after": (a3 or {}).get("status"), "pause_reason": (a3 or {}).get("pauseReason"), "invoke_over_budget": r.get("invoke"),
                "ran_over_budget": not blocked, "overview_status": s4, "overview": h.redact(ov), "raise_status": s5, "resume_status": s6, "resume_body": raw6[:200],
                "ran_after_raise": "fatal" not in r2},
               "works in the free edition" if ("fatal" not in r0 and s2 in (200, 201) and blocked and (a3 or {}).get("status") == "paused" and (a3 or {}).get("pauseReason") == "budget") else "not verified")

    def hire_approval():
        """Approvals: new agents"""
        s1, _, raw1 = h.pc("PATCH", f"/api/companies/{cid}", {"requireBoardApprovalForNewAgents": True})
        body = {"name": f"{G}-second", "role": "general", "adapterType": "process", "adapterConfig": h.agent_config(G + "-hire")}
        s2, d2, raw2 = h.pc("POST", f"/api/companies/{cid}/agents", body)
        s3, d3, raw3 = h.pc("POST", f"/api/companies/{cid}/agent-hires", body)
        hired = (d3 or {}).get("agent") or {}
        appr = (d3 or {}).get("approval") or {}
        s4, pend, _ = h.pc("GET", f"/api/companies/{cid}/approvals?status=pending")
        s5, d5, raw5 = h.pc("POST", f"/api/approvals/{appr.get('id')}/approve", {"decisionNote": "spike"}) if appr.get("id") else (0, None, "no approval id")
        s6, a6, _ = h.pc("GET", f"/api/agents/{hired.get('id')}") if hired.get("id") else (0, None, "")
        h.pc("PATCH", f"/api/companies/{cid}", {"requireBoardApprovalForNewAgents": False})
        record("approvals: hiring an agent", "require approval for new agents, try to create one directly, request a hire, approve it",
               {"setting_status": s1, "direct_create_status": s2, "direct_create_body": raw2[:160], "hire_request_status": s3, "hire_keys": sorted((d3 or {}).keys()),
                "agent_status_before_approval": hired.get("status"), "approval_type": appr.get("type"), "approval_status": appr.get("status"),
                "pending_count": len(pend) if isinstance(pend, list) else None, "approve_status": s5, "approve_body": raw5[:160] if s5 != 200 else "ok",
                "agent_status_after_approval": (a6 or {}).get("status")},
               "works in the free edition" if (s2 == 409 and s3 in (200, 201) and hired.get("status") == "pending_approval" and s5 == 200
                                                 and (a6 or {}).get("status") not in (None, "pending_approval")) else "not verified")

    def activity():
        """Audit log: activity"""
        s, acts, raw = h.pc("GET", f"/api/companies/{cid}/activity?limit=200")
        rows = acts if isinstance(acts, list) else (acts or {}).get("items") or (acts or {}).get("activity") or []
        actions = sorted({str(a.get("action")) for a in rows if isinstance(a, dict)})
        s2, ev, _ = h.gateway_audit(cid)
        want = ["agent.paused", "agent.resumed"]
        record("audit log", "read the company activity log and the tool gateway audit after the probes above",
               {"activity_status": s, "activity_rows": len(rows), "actions_seen": actions[:60], "gateway_audit_events": len(ev),
                "gateway_outcomes": sorted({str(e.get("normalizedOutcome")) for e in ev})},
               "works in the free edition" if (s == 200 and all(w in actions for w in want) and len(ev) > 0) else ("partly works" if s == 200 and rows else "not verified"))

    def terminate():
        """Kill: terminate an agent"""
        s1, d1, raw1 = h.pc("POST", f"/api/agents/{aid}/terminate", {})
        r = h.run_agent(st, G, [{"label": "after-terminate", "tool": "brain_whoami"}], timeout=20)
        record("terminate", "terminate the agent, then trigger a heartbeat",
               {"terminate_status": s1, "agent_status": (d1 or {}).get("status"), "invoke_after": r.get("invoke"), "ran_after_terminate": "fatal" not in r},
               "works in the free edition" if (s1 == 200 and "fatal" in r) else "not verified")

    for fn in (baseline, tool_policy, pause_and_kill, secrets, boundary, spend_cap, hire_approval, activity, terminate):
        guarded(fn)
        (out / "governance.json").write_text(json.dumps({"paperclip_version": (h.pc("GET", "/api/health")[1] or {}).get("version"), "probes": probes}, indent=1))
    return all(p["verdict"] != "failed" for p in probes)
