"""Configuração das instâncias usadas pelo balanceador."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Servidor:
    identificador: int
    hospedeiro: str
    porta: int


SERVIDORES = (
    Servidor(1, "server1", 3002),
    Servidor(2, "server2", 3003),
    Servidor(3, "server3", 3004),
)
