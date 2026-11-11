"""Balanceador HTTP da ShopNow com health check e dois algoritmos."""

import json
import random
from dataclasses import dataclass
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Lock
from urllib.parse import parse_qs, urlsplit


@dataclass(frozen=True)
class Server:
    identifier: int
    host: str
    port: int


SERVERS = (
    Server(1, "server1", 3002),
    Server(2, "server2", 3003),
    Server(3, "server3", 3004),
)


class LoadBalancer:
    def __init__(self, servers):
        self.servers = servers
        self.round_robin_index = 0
        self.lock = Lock()

    @staticmethod
    def is_healthy(server):
        try:
            connection = HTTPConnection(server.host, server.port, timeout=1)
            connection.request("GET", "/health")
            response = connection.getresponse()
            response.read()
            connection.close()
            return response.status == 200
        except OSError:
            return False

    def healthy_servers(self):
        return [server for server in self.servers if self.is_healthy(server)]

    def choose(self, algorithm):
        healthy = self.healthy_servers()
        if not healthy:
            return None
        if algorithm == "random":
            return random.choice(healthy)
        with self.lock:
            server = healthy[self.round_robin_index % len(healthy)]
            self.round_robin_index += 1
            return server


BALANCER = LoadBalancer(SERVERS)


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

        server = BALANCER.choose(algorithm)
        if server is None:
            self.send_json(503, {"error": "all ShopNow servers are unavailable"})
            return
        self.proxy_to(server)

    def send_health_status(self):
        status = [
            {"id": server.identifier, "host": server.host, "active": BALANCER.is_healthy(server)}
            for server in SERVERS
        ]
        code = 200 if any(server["active"] for server in status) else 503
        self.send_json(code, {"servers": status})

    def proxy_to(self, server):
        try:
            connection = HTTPConnection(server.host, server.port, timeout=3)
            connection.request("GET", self.path)
            response = connection.getresponse()
            body = response.read()
            content_type = response.getheader("Content-Type", "application/octet-stream")
            connection.close()
        except OSError:
            self.send_json(502, {"error": "selected server became unavailable"})
            return

        self.send_response(response.status)
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
