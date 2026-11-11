"""Modelos de domínio do balanceador."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Server:
    """Representa uma instância disponível para receber tráfego."""

    identifier: int
    host: str
    port: int
