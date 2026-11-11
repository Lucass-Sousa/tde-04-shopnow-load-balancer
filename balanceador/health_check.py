"""Verificação de disponibilidade das instâncias."""

from http.client import HTTPConnection, HTTPException


def verificar_saude(servidor):
    """Retorna se a instância respondeu com sucesso ao endpoint de saúde."""
    try:
        conexao = HTTPConnection(servidor.hospedeiro, servidor.porta, timeout=1)
        conexao.request("GET", "/health")
        resposta = conexao.getresponse()
        resposta.read()
        return resposta.status == 200
    except (OSError, HTTPException):
        return False
    finally:
        if "conexao" in locals():
            conexao.close()


def servidores_ativos(servidores):
    """Filtra somente as instâncias que estão saudáveis."""
    return [servidor for servidor in servidores if verificar_saude(servidor)]
