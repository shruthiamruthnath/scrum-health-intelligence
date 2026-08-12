from __future__ import annotations

import argparse
import json
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from .service import snapshot

ROOT = Path(__file__).resolve().parent.parent
WEB = ROOT / "web"


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB), **kwargs)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/health": return self.json_response({"status": "ok"})
        if path == "/api/snapshot": return self.json_response(snapshot())
        if path == "/api/risks": return self.json_response(snapshot()["risks"])
        if path == "/api/dependencies": return self.json_response(snapshot()["dependencies"])
        if path == "/api/brief": return self.json_response(snapshot()["brief"])
        if path == "/": self.path = "/index.html"
        return super().do_GET()

    def json_response(self, payload):
        body = json.dumps(payload, default=str).encode()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers(); self.wfile.write(body)

    def log_message(self, fmt, *args):
        print(f"[scrum-health] {self.address_string()} {fmt % args}")


def main():
    parser = argparse.ArgumentParser(description="Run Scrum Health Intelligence")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8080, type=int)
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Scrum Health Intelligence: http://{args.host}:{args.port}")
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()


if __name__ == "__main__": main()

