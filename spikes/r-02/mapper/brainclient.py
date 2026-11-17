"""Tiny client for the permission service: HTTP over TCP or over a Unix socket. Standard library only."""
import http.client, json, os, socket, uuid


class _UnixConn(http.client.HTTPConnection):
    def __init__(self, path):
        super().__init__("localhost", timeout=120)
        self._path = path

    def connect(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.settimeout(120)
        self.sock.connect(self._path)


class Brain:
    def __init__(self, socket_path=None, host="127.0.0.1", port=8900):
        self.socket_path, self.host, self.port = socket_path or os.environ.get("BRAIN_SOCKET"), host, port

    def request(self, method, path, token, body=None):
        conn = _UnixConn(self.socket_path) if self.socket_path else http.client.HTTPConnection(self.host, self.port, timeout=120)
        try:
            conn.request(method, path, body=None if body is None else json.dumps(body),
                         headers={"Content-Type": "application/json", "Authorization": "Bearer " + token})
            r = conn.getresponse()
            raw = r.read().decode()
            return r.status, (json.loads(raw) if raw else None)
        finally:
            conn.close()

    def admin(self, method, path, body=None, token=None):
        status, data = self.request(method, path, token or os.environ.get("BRAIN_ADMIN_TOKEN", ""), body)
        if status != 200:
            raise RuntimeError(f"admin {path}: {status} {data}")
        return data

    def tool(self, token, name, args=None):
        """One MCP tools/call. Returns (ok, payload)."""
        status, data = self.request("POST", "/mcp", token, {"jsonrpc": "2.0", "id": str(uuid.uuid4()), "method": "tools/call",
                                                            "params": {"name": name, "arguments": args or {}}})
        if status != 200 or "result" not in (data or {}):
            return False, {"error": f"http {status}"}
        res = data["result"]
        return (not res.get("isError")), json.loads(res["content"][0]["text"])
