"""Verificação de disponibilidade das instâncias."""

from http.client import HTTPConnection, HTTPException


def is_healthy(server):
    """Retorna se a instância respondeu com sucesso ao endpoint de saúde."""
    try:
        connection = HTTPConnection(server.host, server.port, timeout=1)
        connection.request("GET", "/health")
        response = connection.getresponse()
        response.read()
        return response.status == 200
    except (OSError, HTTPException):
        return False
    finally:
        if "connection" in locals():
            connection.close()


def healthy_servers(servers):
    """Filtra somente as instâncias que estão saudáveis."""
    return [server for server in servers if is_healthy(server)]
