"""Camada HTTP e orquestração do balanceador da ShopNow."""

import json
from http.client import HTTPConnection, HTTPException
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

from algorithms import SelecionadorServidor
from health_check import servidores_ativos, verificar_saude
from servers import SERVIDORES

SELECIONADOR = SelecionadorServidor()


class ManipuladorRequisicao(BaseHTTPRequestHandler):
    def do_GET(self):
        url_analisada = urlsplit(self.path)
        if url_analisada.path == "/health":
            self.enviar_status_saude()
            return

        parametros = parse_qs(url_analisada.query)
        algoritmo = parametros.get("algorithm", ["round-robin"])[0]
        if algoritmo not in {"round-robin", "random"}:
            self.enviar_json(400, {"erro": "algorithm deve ser round-robin ou random"})
            return

        servidor = SELECIONADOR.escolher(servidores_ativos(SERVIDORES), algoritmo)
        if servidor is None:
            self.enviar_json(503, {"erro": "todos os servidores ShopNow estao indisponiveis"})
            return
        self.encaminhar_requisicao(servidor, algoritmo)

    def enviar_status_saude(self):
        status_servidores = [
            {"id": servidor.identificador, "host": servidor.hospedeiro, "ativo": verificar_saude(servidor)}
            for servidor in SERVIDORES
        ]
        codigo = 200 if any(servidor["ativo"] for servidor in status_servidores) else 503
        self.enviar_json(codigo, {"servidores": status_servidores})

    def encaminhar_requisicao(self, servidor, algoritmo):
        try:
            conexao = HTTPConnection(servidor.hospedeiro, servidor.porta, timeout=3)
            conexao.request("GET", self.path)
            resposta = conexao.getresponse()
            codigo = resposta.status
            tipo_conteudo = resposta.getheader("Content-Type", "application/octet-stream")
            corpo = resposta.read()
            conexao.close()
        except (OSError, HTTPException):
            self.enviar_json(502, {"erro": "o servidor selecionado ficou indisponivel"})
            return

        self.send_response(codigo)
        self.send_header("Content-Type", tipo_conteudo)
        self.send_header("Content-Length", str(len(corpo)))
        self.send_header("X-ShopNow-Server", str(servidor.identificador))
        self.end_headers()
        self.wfile.write(corpo)
        print(f"[Balanceador] {algoritmo} -> Servidor {servidor.identificador}", flush=True)

    def enviar_json(self, codigo, dados):
        corpo = json.dumps(dados).encode()
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def log_message(self, format, *args):
        return


def main():
    servidor_http = ThreadingHTTPServer(("0.0.0.0", 3001), ManipuladorRequisicao)
    print("Balanceador ShopNow escutando na porta 3001", flush=True)
    servidor_http.serve_forever()


if __name__ == "__main__":
    main()
