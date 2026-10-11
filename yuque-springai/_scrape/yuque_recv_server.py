# -*- coding: utf-8 -*-
"""Local receiver for yuque scraping: accepts JSON posts from the browser page."""
import json
import os
import re
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

OUT_DIR = r"D:\aiface\yuque-springai"


def safe_name(name: str) -> str:
    name = re.sub(r'[\\/:*?"<>|\r\n\t]', " ", name).strip()
    name = re.sub(r"\s+", " ", name)
    return name[:80]


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        sys.stderr.write("[recv] " + fmt % args + "\n")

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Private-Network", "true")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        if self.path.startswith("/ping"):
            body = b"pong"
            self.send_response(200)
            self._cors()
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_error(404)

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length)
            payload = json.loads(raw.decode("utf-8"))
            cmd = payload.get("cmd")
            if cmd == "save":
                rel = payload["path"]  # already sanitized relative path with /
                content = payload["content"]
                full = os.path.join(OUT_DIR, rel.replace("/", os.sep))
                os.makedirs(os.path.dirname(full), exist_ok=True)
                with open(full, "w", encoding="utf-8", newline="\n") as f:
                    f.write(content)
                reply = json.dumps({"ok": True, "path": rel, "chars": len(content)}).encode()
            elif cmd == "log":
                sys.stderr.write("[page] " + str(payload.get("msg")) + "\n")
                reply = b'{"ok":true}'
            else:
                reply = b'{"ok":false,"error":"unknown cmd"}'
            self.send_response(200)
            self._cors()
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(reply)))
            self.end_headers()
            self.wfile.write(reply)
        except Exception as e:
            reply = json.dumps({"ok": False, "error": str(e)}).encode("utf-8")
            self.send_response(200)
            self._cors()
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(reply)))
            self.end_headers()
            self.wfile.write(reply)


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    srv = ThreadingHTTPServer(("127.0.0.1", 8765), Handler)
    print("receiver on http://127.0.0.1:8765 ->", OUT_DIR, flush=True)
    srv.serve_forever()
