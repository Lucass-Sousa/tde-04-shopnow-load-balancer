"""Encaminhamento de requisições para a instância selecionada."""

from http.client import HTTPConnection, HTTPException


def forward_request(server, path):
    """Executa uma requisição GET na instância e devolve sua resposta."""
    connection = None
    try:
        connection = HTTPConnection(server.host, server.port, timeout=3)
        connection.request("GET", path)
        response = connection.getresponse()
        return (
            response.status,
            response.getheader("Content-Type", "application/octet-stream"),
            response.read(),
        )
    except (OSError, HTTPException) as error:
        raise ConnectionError("selected server became unavailable") from error
    finally:
        if connection:
            connection.close()
