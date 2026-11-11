"""Servidor HTTP simples usado por cada instância da ShopNow."""

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from string import Template
from threading import Lock


CAMINHO_TEMPLATE = Path(__file__).parent / "templates" / "index.html"
TEMPLATE_PAGINA = Template(CAMINHO_TEMPLATE.read_text(encoding="utf-8"))


class ServidorShopNow(ThreadingHTTPServer):
    def __init__(self, endereco, manipulador, identificador):
        super().__init__(endereco, manipulador)
        self.identificador = identificador
        self.total_requisicoes = 0
        self.trava_requisicoes = Lock()


class ManipuladorRequisicao(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.enviar_json({"status": "ok", "servidor_id": self.server.identificador})
            return

        with self.server.trava_requisicoes:
            self.server.total_requisicoes += 1
            numero_requisicao = self.server.total_requisicoes

        pagina = self.montar_pagina(numero_requisicao)
        corpo = pagina.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def enviar_json(self, dados):
        corpo = json.dumps(dados).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def montar_pagina(self, numero_requisicao):
        return TEMPLATE_PAGINA.substitute(
            identificador=self.server.identificador,
            numero_requisicao=numero_requisicao,
        )

    def log_message(self, format, *args):
        return


def main():
    argumentos = argparse.ArgumentParser()
    argumentos.add_argument("--id", type=int, required=True)
    argumentos.add_argument("--port", type=int, required=True)
    opcoes = argumentos.parse_args()

    servidor_http = ServidorShopNow(("0.0.0.0", opcoes.port), ManipuladorRequisicao, opcoes.id)
    print(f"Servidor ShopNow {opcoes.id} escutando na porta {opcoes.port}", flush=True)
    servidor_http.serve_forever()


if __name__ == "__main__":
    main()
