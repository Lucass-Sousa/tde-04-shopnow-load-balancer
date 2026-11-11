"""Camada HTTP e orquestração do balanceador da ShopNow."""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

from algorithms import ServerSelector
from config import SERVERS
from health_check import healthy_servers, is_healthy
from proxy import forward_request

SELECTOR = ServerSelector()


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlsplit(self.path)
        if parsed_url.path == "/health":
            self.send_health_status()
            return

        parameters = parse_qs(parsed_url.query)
        algorithm = parameters.get("algorithm", ["round-robin"])[0]
        if algorithm not in {"round-robin", "random"}:
            self.send_json(400, {"error": "algorithm must be round-robin or random"})
            return

        server = SELECTOR.choose(healthy_servers(SERVERS), algorithm)
        if server is None:
            self.send_json(503, {"error": "all ShopNow servers are unavailable"})
            return
        self.proxy_to(server)

    def send_health_status(self):
        status = [
            {"id": server.identifier, "host": server.host, "active": is_healthy(server)}
            for server in SERVERS
        ]
        code = 200 if any(server["active"] for server in status) else 503
        self.send_json(code, {"servers": status})

    def proxy_to(self, server):
        try:
            status, content_type, body = forward_request(server, self.path)
        except ConnectionError:
            self.send_json(502, {"error": "selected server became unavailable"})
            return

        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-ShopNow-Server", str(server.identifier))
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, code, payload):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        return


def main():
    server = ThreadingHTTPServer(("0.0.0.0", 3001), RequestHandler)
    print("ShopNow load balancer listening on port 3001", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
