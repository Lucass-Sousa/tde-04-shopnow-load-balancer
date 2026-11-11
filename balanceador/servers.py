"""Configuração das instâncias usadas pelo balanceador."""

from dataclasses import dataclass


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
