.PHONY: help up down logs init git-start server1 server2 server3

help:  ## Mostrar esta ajuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "} {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

up:  ## Subir todos os containers Docker
	docker-compose up -d

down:  ## Derribar todos os containers
	docker-compose down

logs:  ## Ver logs dos containers
	docker-compose logs -f

init:  ## Inicializar estrutura do projeto (pastas, git, etc)
	@mkdir -p balanceador servers/server1 servers/server2 servers/server3
	@git init
	@echo "# TDE-04 - ShopNow Load Balancer" > README.md
	@echo "" >> README.md
	@echo "Projeto de balanceamento de carga para startup ShopNow." >> README.md
	@echo "3 instâncias PHP + balanceador com 2 algoritmos." >> README.md
	@git add .
	@git commit -m "feat: Estrutura base do projeto - pastas e readme"
	@echo "✅ Projeto inicializado!"

## Servidores

server1:  ## Subir apenas servidor 1
	docker-compose up -d server1

server2:  ## Subir apenas servidor 2
	docker-compose up -d server2

server3:  ## Subir apenas servidor 3
	docker-compose up -d server3