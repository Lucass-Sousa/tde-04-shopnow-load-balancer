.PHONY: help up down logs server1 server2 server3 stop-server1 stop-server2 stop-server3 test-load

help:  ## Mostrar esta ajuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "} {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

up:  ## Subir todos os containers Docker
	@docker compose up -d --build --quiet-build --wait > /dev/null
	@echo ""
	@echo "ShopNow esta disponivel em:"
	@echo "  Aplicacao:   http://localhost:3001/"
	@echo "  Dashboard:   http://localhost:3001/dashboard"
	@echo "  Health check: http://localhost:3001/health"
	@echo "  Aleatorio:   http://localhost:3001/?algorithm=random"

down:  ## Derribar todos os containers
	docker compose down

logs:  ## Ver logs dos containers
	docker compose logs -f

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

test-load:  ## Executar teste de carga com Apache Benchmark
	ab -n 1000 -c 50 http://localhost:3001/
