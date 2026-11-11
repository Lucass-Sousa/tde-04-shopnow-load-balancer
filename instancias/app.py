"""Servidor HTTP simples usado por cada instância da ShopNow."""

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Lock


class ShopNowServer(ThreadingHTTPServer):
    def __init__(self, address, handler, server_id):
        super().__init__(address, handler)
        self.server_id = server_id
        self.requests = 0
        self.requests_lock = Lock()


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        with self.server.requests_lock:
            self.server.requests += 1
            request_number = self.server.requests

        payload = {
            "service": "ShopNow",
            "server_id": self.server.server_id,
            "request_number": request_number,
            "path": self.path,
        }
        body = json.dumps(payload).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=int, required=True)
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()

    server = ShopNowServer(("0.0.0.0", args.port), RequestHandler, args.id)
    print(f"ShopNow server {args.id} listening on port {args.port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
