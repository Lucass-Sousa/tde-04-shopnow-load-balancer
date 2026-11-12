"""Gera requisições e mostra a distribuição no terminal."""

import argparse
import os
import sys
import time
from collections import Counter
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


LARGURA_BARRA = 30
TERMINAL_INTERATIVO = sys.stdout.isatty()
RESET = "\033[0m"
CORES = {
    "titulo": "\033[96m",
    "progresso": "\033[93m",
    1: "\033[94m",
    2: "\033[92m",
    3: "\033[95m",
    "erro": "\033[91m",
}


def colorir(texto, cor):
    return f"{CORES[cor]}{texto}{RESET}" if TERMINAL_INTERATIVO else texto


def barra(valor, total, cor):
    quantidade = round((valor / total) * LARGURA_BARRA) if total else 0
    preenchida = colorir("█" * quantidade, cor)
    return preenchida + "·" * (LARGURA_BARRA - quantidade)


def mostrar_painel(algoritmo, quantidade, atual, contadores, falhas, identificador, ultima_resposta):
    progresso = (atual / quantidade) * 100
    if TERMINAL_INTERATIVO:
        os.system("clear")
    print(colorir(f"ShopNow | Algoritmo: {algoritmo}", "titulo"))
    print(f"Progresso: [{barra(atual, quantidade, 'progresso')}] {atual}/{quantidade} ({progresso:.0f}%)")
    print(f"Requisição atual: {identificador}")
    print(f"Última resposta: {ultima_resposta}")
    print()
    for identificador in (1, 2, 3):
        atendidas = contadores[identificador]
        percentual = (atendidas / atual) * 100 if atual else 0
        print(
            colorir(
                f"Servidor {identificador}: [{barra(atendidas, quantidade, identificador)}] "
                f"{atendidas} ({percentual:.0f}%)",
                identificador,
            )
        )
    if falhas:
        print(colorir(f"\nRequisições sem servidor disponível: {falhas}", "erro"))
    print("\nAcompanhe as decisões detalhadas em outro terminal com: make logs", flush=True)


def enviar_requisicao(algoritmo, identificador):
    endereco = f"http://localhost:3001/?algorithm={algoritmo}&requisicao_id={identificador}"
    try:
        with urlopen(endereco, timeout=5) as resposta:
            return resposta.headers.get("X-ShopNow-Server")
    except (HTTPError, URLError, TimeoutError):
        return None


def main():
    argumentos = argparse.ArgumentParser()
    argumentos.add_argument("--algoritmo", choices=("round-robin", "least-conn"), required=True)
    argumentos.add_argument("--quantidade", type=int, required=True)
    argumentos.add_argument("--intervalo", type=float, required=True)
    opcoes = argumentos.parse_args()

    contadores = Counter()
    falhas = 0
    for atual in range(1, opcoes.quantidade + 1):
        identificador = f"REQ-{atual:03d}"
        servidor = enviar_requisicao(opcoes.algoritmo, identificador)
        if servidor:
            contadores[int(servidor)] += 1
            ultima_resposta = f"{identificador} → Servidor {servidor}"
        else:
            falhas += 1
            ultima_resposta = f"{identificador} → Nenhum servidor disponível"
        mostrar_painel(
            opcoes.algoritmo,
            opcoes.quantidade,
            atual,
            contadores,
            falhas,
            identificador,
            ultima_resposta,
        )
        if atual < opcoes.quantidade:
            time.sleep(opcoes.intervalo)


if __name__ == "__main__":
    main()
