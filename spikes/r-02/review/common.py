"""REV-01 review: helpers shared by the review tests. Standard library only.

The service under test is the unmodified ../service/server.mjs with ../service/schema.sql.
Environment: BRAIN_URL, BRAIN_ADMIN_TOKEN, BRAIN_APP_DSN (the same three the existing tests use).
All data is made up. The tokens are the fixture's test values.
"""
import http.client
import json
import os
import pathlib
import subprocess
import urllib.error
import urllib.parse
import urllib.request
import uuid

URL = os.environ.get("BRAIN_URL", "http://127.0.0.1:8900")
ADMIN = os.environ.get("BRAIN_ADMIN_TOKEN", "")
APP_DSN = os.environ.get("BRAIN_APP_DSN", "")
FIXTURE = json.loads((pathlib.Path(__file__).resolve().parent.parent / "tests" / "fixture.json").read_text())
TOKENS = {(p["org"], p["actor"]): p["token"] for p in FIXTURE["principals"]}
T_PERSONAL, T_MGMT = TOKENS[("personal", "agent")], TOKENS[("mgmt", "agent")]
T_TOVELI, T_TOVELI_HUMAN, T_SIBLING = TOKENS[("toveli", "agent")], TOKENS[("toveli", "human")], TOKENS[("sibling", "agent")]


def http_call(method, path, token=None, body=None, headers=None):
    req = urllib.request.Request(URL + path, method=method, data=None if body is None else json.dumps(body).encode())
    req.add_header("Content-Type", "application/json")
    if token is not None:
        req.add_header("Authorization", "Bearer " + token)
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


def raw_request(method, path, header_lines, body=b""):
    """One request with header values given as bytes, so a value may hold bytes above 0x7f."""
    u = urllib.parse.urlparse(URL)
    c = http.client.HTTPConnection(u.hostname, u.port, timeout=30)
    c.putrequest(method, path)
    for k, v in header_lines:
        c.putheader(k, v)
    if body:
        c.putheader("Content-Length", str(len(body)))
    c.endheaders(body or None)
    r = c.getresponse()
    data = r.read().decode("utf-8", "replace")
    c.close()
    return r.status, data


def rpc(token, name, arguments, headers=None):
    """A tools/call exactly as given: nothing is added to the arguments. Returns (http status, raw text)."""
    return http_call("POST", "/mcp", token, {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": name, "arguments": arguments}}, headers)


def call(token, tool, args=None):
    """One MCP tools/call with a fresh request ID. Returns (ok, payload, raw_text)."""
    status, raw = rpc(token, tool, dict(args or {}, request_id=str(uuid.uuid4())))
    if status != 200:
        return False, {"http": status}, raw
    msg = json.loads(raw)
    if "error" in msg:
        return False, msg["error"], raw
    res = msg["result"]
    text = res["content"][0]["text"] if res.get("content") else "{}"
    try:
        payload = json.loads(text)
    except ValueError:
        payload = {"text": text}
    return (not res.get("isError", False)), payload, raw


def admin(path, body=None, method="POST"):
    status, raw = http_call(method, path, ADMIN, body)
    assert status == 200, f"admin {path} -> {status} {raw[:300]}"
    return json.loads(raw) if raw else {}


def reset(fixture=None, **settings):
    fx = json.loads(json.dumps(fixture or FIXTURE))
    fx.setdefault("settings", {}).update(settings)
    return admin("/admin/reset", fx)


def audit_rows(since_id=0):
    return admin(f"/admin/audit?since_id={since_id}", method="GET")["rows"]


def last_audit_id():
    return max([r["id"] for r in audit_rows()] or [0])


def psql(sql, dsn=None):
    out = subprocess.run(["psql", dsn or APP_DSN, "-X", "-q", "-A", "-t", "-v", "ON_ERROR_STOP=1", "-c", sql],
                         capture_output=True, text=True, timeout=120)
    return out.returncode, (out.stdout + out.stderr).strip()


def page_id(token, marker):
    ok, payload, _ = call(token, "brain_search", {"query": marker})
    assert ok and payload["pages"], f"owner cannot find its own page {marker}"
    return payload["pages"][0]["id"]
