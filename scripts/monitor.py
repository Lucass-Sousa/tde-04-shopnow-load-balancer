"""Gera requisições e mostra a distribuição no terminal."""

import argparse
import os
import sys
import time
from collections import Counter
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


LARGURA_BARRA = 30


def barra(valor, total):
    quantidade = round((valor / total) * LARGURA_BARRA) if total else 0
    return "█" * quantidade + "·" * (LARGURA_BARRA - quantidade)


def mostrar_painel(algoritmo, quantidade, atual, contadores, falhas):
    progresso = (atual / quantidade) * 100
    if sys.stdout.isatty():
        os.system("clear")
    print(f"ShopNow | Algoritmo: {algoritmo}")
    print(f"Progresso: [{barra(atual, quantidade)}] {atual}/{quantidade} ({progresso:.0f}%)")
    print()
    for identificador in (1, 2, 3):
        atendidas = contadores[identificador]
        percentual = (atendidas / atual) * 100 if atual else 0
        print(f"Servidor {identificador}: [{barra(atendidas, quantidade)}] {atendidas} ({percentual:.0f}%)")
    if falhas:
        print(f"\nRequisições sem servidor disponível: {falhas}")
    print("\nAcompanhe as decisões detalhadas em outro terminal com: make logs", flush=True)


def enviar_requisicao(algoritmo):
    endereco = f"http://localhost:3001/?algorithm={algoritmo}"
    try:
        with urlopen(endereco, timeout=3) as resposta:
            return resposta.headers.get("X-ShopNow-Server")
    except (HTTPError, URLError):
        return None


def main():
    argumentos = argparse.ArgumentParser()
    argumentos.add_argument("--algoritmo", choices=("round-robin", "random"), required=True)
    argumentos.add_argument("--quantidade", type=int, required=True)
    argumentos.add_argument("--intervalo", type=float, required=True)
    opcoes = argumentos.parse_args()

    contadores = Counter()
    falhas = 0
    for atual in range(1, opcoes.quantidade + 1):
        servidor = enviar_requisicao(opcoes.algoritmo)
        if servidor:
            contadores[int(servidor)] += 1
        else:
            falhas += 1
        mostrar_painel(opcoes.algoritmo, opcoes.quantidade, atual, contadores, falhas)
        if atual < opcoes.quantidade:
            time.sleep(opcoes.intervalo)


if __name__ == "__main__":
    main()
