.PHONY: help install up down logs request start server1 server2 server3 stop-server1 stop-server2 stop-server3 demo-round-robin demo-random test-demo test-load

ALGORITMO ?= round-robin
INTERVALO ?= 1

help:  ## Mostrar esta ajuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "} {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Instalar Apache Benchmark para os testes de carga
	sudo apt update
	sudo apt install -y apache2-utils

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

request:  ## Enviar uma requisicao (use ALGORITMO=random para Random)
	@curl -s "http://localhost:3001/?algorithm=$(ALGORITMO)"
	@echo ""

start:  ## Enviar requisicoes uma por vez (Ctrl+C para parar)
	@while true; do \
		curl -s "http://localhost:3001/?algorithm=$(ALGORITMO)"; \
		echo; \
		sleep $(INTERVALO); \
	done

## Servidores

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

demo-round-robin:  ## Demonstrar 9 requisicoes sequenciais com Round Robin
	@for requisicao in 1 2 3 4 5 6 7 8 9; do \
		curl -s http://localhost:3001/; \
		echo; \
	done

demo-random:  ## Demonstrar 9 requisicoes sequenciais com algoritmo Random
	@for requisicao in 1 2 3 4 5 6 7 8 9; do \
		curl -s 'http://localhost:3001/?algorithm=random'; \
		echo; \
	done

test-demo:  ## Gerar 30 requisicoes para acompanhar nos logs
	ab -q -n 30 -c 3 http://localhost:3001/

test-load:  ## Executar teste de carga com Apache Benchmark
	ab -n 1000 -c 50 http://localhost:3001/
