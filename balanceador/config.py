"""Configuração das instâncias gerenciadas pelo balanceador."""

from models import Server


SERVERS = (
    Server(1, "server1", 3002),
    Server(2, "server2", 3003),
    Server(3, "server3", 3004),
)
