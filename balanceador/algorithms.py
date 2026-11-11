"""Algoritmos de distribuição de carga."""

import random
from threading import Lock


class SelecionadorServidor:
    """Seleciona uma instância saudável conforme o algoritmo solicitado."""

    def __init__(self):
        self.indice_round_robin = 0
        self.trava = Lock()

    def escolher(self, servidores, algoritmo):
        if not servidores:
            return None
        if algoritmo == "random":
            return random.choice(servidores)
        return self._escolher_round_robin(servidores)

    def _escolher_round_robin(self, servidores):
        with self.trava:
            servidor = servidores[self.indice_round_robin % len(servidores)]
            self.indice_round_robin += 1
            return servidor
