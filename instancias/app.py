"""Servidor HTTP simples usado por cada instância da ShopNow."""

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Lock


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
        identificador = self.server.identificador
        return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ShopNow | Servidor {identificador}</title>
  <style>
    * {{ box-sizing: border-box; }}
    body {{
      align-items: center;
      background: linear-gradient(135deg, #111827, #312e81);
      color: #f9fafb;
      display: flex;
      font-family: Arial, sans-serif;
      justify-content: center;
      margin: 0;
      min-height: 100vh;
      padding: 24px;
    }}
    main {{
      background: rgba(255, 255, 255, .1);
      border: 1px solid rgba(255, 255, 255, .2);
      border-radius: 20px;
      box-shadow: 0 20px 50px rgba(0, 0, 0, .25);
      max-width: 520px;
      padding: 42px;
      text-align: center;
      width: 100%;
    }}
    .marca {{ color: #a5b4fc; font-size: 1.1rem; font-weight: bold; letter-spacing: 2px; }}
    h1 {{ font-size: 2.2rem; margin: 18px 0 10px; }}
    .servidor {{ color: #86efac; font-size: 1.2rem; margin: 0; }}
    .cartao {{ background: rgba(17, 24, 39, .5); border-radius: 12px; margin-top: 28px; padding: 20px; }}
    .numero {{ color: #fbbf24; display: block; font-size: 2.4rem; font-weight: bold; margin-top: 8px; }}
    small {{ color: #d1d5db; }}
  </style>
</head>
<body>
  <main>
    <div class="marca">SHOPNOW</div>
    <h1>Compra processada com sucesso</h1>
    <p class="servidor">Atendido pelo servidor {identificador}</p>
    <div class="cartao">
      <small>Requisições atendidas por esta instância</small>
      <span class="numero">{numero_requisicao}</span>
    </div>
  </main>
</body>
</html>"""

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
