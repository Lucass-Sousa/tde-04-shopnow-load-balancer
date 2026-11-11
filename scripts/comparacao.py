"""Compara Round Robin e Random no mesmo painel do terminal."""

import argparse
import os
import time
from collections import Counter

from monitor import TERMINAL_INTERATIVO, barra, colorir, enviar_requisicao


ALGORITMOS = (("round-robin", "RR"), ("random", "RND"))


def mostrar_distribuicao(algoritmo, contadores, quantidade, cor):
    print(colorir(algoritmo, cor))
    for identificador in (1, 2, 3):
        atendidas = contadores[identificador]
        percentual = (atendidas / quantidade) * 100 if quantidade else 0
        print(f"  Servidor {identificador}: [{barra(atendidas, quantidade, cor)}] {atendidas} ({percentual:.0f}%)")


def mostrar_painel(atual, quantidade, contadores, falhas, ultima_resposta):
    if TERMINAL_INTERATIVO:
        os.system("clear")
    print(colorir("ShopNow | Comparação de algoritmos", "titulo"))
    print(f"Ciclo: {atual}/{quantidade} | Total de requisições: {atual * 2}")
    print(f"Última resposta: {ultima_resposta}\n")
    mostrar_distribuicao("Round Robin", contadores["round-robin"], atual, 1)
    print()
    mostrar_distribuicao("Random", contadores["random"], atual, 3)
    if falhas:
        print(colorir(f"\nRequisições sem servidor disponível: {falhas}", "erro"))
    print("\nAcompanhe as decisões detalhadas em outro terminal com: make logs", flush=True)


def main():
    argumentos = argparse.ArgumentParser()
    argumentos.add_argument("--quantidade", type=int, required=True)
    argumentos.add_argument("--intervalo", type=float, required=True)
    opcoes = argumentos.parse_args()

    contadores = {algoritmo: Counter() for algoritmo, _ in ALGORITMOS}
    falhas = 0
    ultima_resposta = "Aguardando primeira requisição"
    for atual in range(1, opcoes.quantidade + 1):
        for algoritmo, prefixo in ALGORITMOS:
            identificador = f"{prefixo}-{atual:03d}"
            servidor = enviar_requisicao(algoritmo, identificador)
            if servidor:
                contadores[algoritmo][int(servidor)] += 1
                ultima_resposta = f"{identificador} → Servidor {servidor}"
            else:
                falhas += 1
                ultima_resposta = f"{identificador} → Nenhum servidor disponível"
        mostrar_painel(atual, opcoes.quantidade, contadores, falhas, ultima_resposta)
        if atual < opcoes.quantidade:
            time.sleep(opcoes.intervalo)


if __name__ == "__main__":
    main()
