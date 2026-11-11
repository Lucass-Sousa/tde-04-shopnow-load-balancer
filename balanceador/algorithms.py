"""Algoritmos de distribuição de carga."""

import random
from threading import Lock


class ServerSelector:
    """Seleciona uma instância saudável conforme o algoritmo solicitado."""

    def __init__(self):
        self.round_robin_index = 0
        self.lock = Lock()

    def choose(self, servers, algorithm):
        if not servers:
            return None
        if algorithm == "random":
            return random.choice(servers)
        return self._round_robin(servers)

    def _round_robin(self, servers):
        with self.lock:
            server = servers[self.round_robin_index % len(servers)]
            self.round_robin_index += 1
            return server
