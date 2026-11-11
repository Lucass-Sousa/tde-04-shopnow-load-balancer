.PHONY: help install up down logs request start start-round-robin start-random start-comparacao validar-env server1 server2 server3 stop-server1 stop-server2 stop-server3 test-demo test-load test-load-round-robin test-load-random

############################################################
# CONFIGURAÇÃO DA DEMONSTRAÇÃO
############################################################
-include .env

ALGORITMO ?= round-robin

############################################################
# AJUDA E DEPENDÊNCIAS
############################################################
help:  ## Mostrar esta ajuda
	@grep -h -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "} {printf "\033[36m%-24s\033[0m %s\n", $$1, $$2}'

install:  ## Instalar Apache Benchmark para os testes de carga
	sudo apt update
	sudo apt install -y apache2-utils

############################################################
# CICLO DE VIDA DA APLICAÇÃO
############################################################
up:  ## Subir todos os containers Docker
	@docker compose up -d --build --quiet-build --wait > /dev/null
	@echo ""
	@echo "ShopNow esta disponivel em:"
	@echo "  Aplicacao:   http://localhost:3001/"
	@echo "  Health check: http://localhost:3001/health"
	@echo "  Aleatorio:   http://localhost:3001/?algorithm=random"

down:  ## Derribar todos os containers
	docker compose down

logs:  ## Ver logs dos containers
	docker compose logs -f --tail=0

############################################################
# DEMONSTRAÇÕES NO TERMINAL
############################################################
request:  ## Enviar uma requisicao (ALGORITMO=random para Random)
	@servidor=$$(curl -s -D - -o /dev/null "http://localhost:3001/?algorithm=$(ALGORITMO)" | awk -F ': ' '/^X-ShopNow-Server:/ {gsub("\r", "", $$2); print $$2}'); \
	if [ -n "$$servidor" ]; then echo "[Resposta] Servidor $$servidor"; else echo "[Resposta] Nenhum servidor disponivel"; fi

validar-env:
	@if [ ! -f .env ]; then echo "Erro: arquivo .env nao encontrado. Execute: cp .env.example .env"; exit 1; fi
	@if [ -z "$(QUANTIDADE)" ] || [ -z "$(INTERVALO)" ]; then echo "Erro: preencha QUANTIDADE e INTERVALO no arquivo .env"; exit 1; fi

start: validar-env
	@python3 scripts/monitor.py --algoritmo $(ALGORITMO) --quantidade $(QUANTIDADE) --intervalo $(INTERVALO)

start-round-robin:  ## Iniciar requisicoes com algoritmo Round Robin
	@$(MAKE) --no-print-directory start ALGORITMO=round-robin

start-random:  ## Iniciar requisicoes com algoritmo Random
	@$(MAKE) --no-print-directory start ALGORITMO=random

start-comparacao: validar-env  ## Comparar Round Robin e Random no mesmo painel
	@python3 scripts/comparacao.py --quantidade $(QUANTIDADE) --intervalo $(INTERVALO)

############################################################
# GERENCIAMENTO DOS SERVIDORES
############################################################
server1:  ## Subir apenas servidor 1
	docker compose up -d server1

server2:  ## Subir apenas servidor 2
	docker compose up -d server2

server3:  ## Subir apenas servidor 3
	docker compose up -d server3

stop-server1:  ## Simular falha do servidor 1
	docker compose stop server1

stop-server2:  ## Simular falha do servidor 2
	docker compose stop server2

stop-server3:  ## Simular falha do servidor 3
	docker compose stop server3

############################################################
# TESTES DE CARGA
############################################################
test-demo:  ## Gerar 30 requisicoes para acompanhar nos logs
	ab -q -l -n 30 -c 3 http://localhost:3001/

test-load:  ## Executar teste de carga Round Robin (atalho)
	@$(MAKE) --no-print-directory test-load-round-robin

test-load-round-robin:  ## Executar carga Apache Benchmark com Round Robin
	ab -l -n 1000 -c 50 http://localhost:3001/

test-load-random:  ## Executar carga Apache Benchmark com Random
	ab -l -n 1000 -c 50 'http://localhost:3001/?algorithm=random'
