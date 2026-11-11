# TDE-04 - ShopNow Load Balancer

Balanceador de carga em Python para três instâncias da ShopNow.

## Recursos

- Três instâncias independentes do site (`server1`, `server2` e `server3`);
- Health check HTTP em cada requisição;
- Algoritmos Round Robin e Random;
- Proxy HTTP: o cliente acessa somente o balanceador;
- Simulação de falha de instâncias com Docker Compose.

## Organização do balanceador

Cada módulo tem uma responsabilidade única, sem fragmentar excessivamente o projeto:

- `app.py`: recebe a requisição HTTP, coordena os demais módulos e encaminha a chamada;
- `servers.py`: define as instâncias monitoradas;
- `health_check.py`: verifica a disponibilidade das instâncias;
- `algorithms.py`: escolhe uma instância por Round Robin ou Random;

## Execução

```bash
make install
make up
curl http://localhost:3001/
```

O algoritmo padrão é Round Robin. Para selecionar o aleatório, use:

```bash
curl 'http://localhost:3001/?algorithm=random'
```

O endpoint `http://localhost:3001/health` mostra quais instâncias estão disponíveis.

## Acompanhamento pelo terminal

Em um terminal, execute `make logs`. Ele exibirá somente as novas escolhas do balanceador e os atendimentos das instâncias.

Em outro terminal, faça demonstrações curtas e fáceis de acompanhar:

```bash
make demo-round-robin
make demo-random
```

O primeiro deve alternar os servidores em ciclo; o segundo deve escolhê-los em ordem variável. Para gerar 30 requisições concorrentes, use `make test-demo`. Para o teste de carga completo, use `make test-load`.

Para enviar e observar uma requisição por vez, use. O terminal exibirá somente o servidor que respondeu:

```bash
make request
make request ALGORITMO=random
```

Para enviar requisições uma por vez com intervalo configurável, crie seu arquivo de ambiente e edite os valores:

```bash
cp .env.example .env
```

Exemplo de `.env`:

```text
QUANTIDADE=10
INTERVALO=1
```

Depois, escolha o algoritmo pelo Makefile:

```bash
make start-round-robin
make start-random
```

O arquivo `.env` é obrigatório para `make start`; não há valores padrão para quantidade ou intervalo.

## Simulação de falha

```bash
make stop-server2
curl http://localhost:3001/health
curl http://localhost:3001/
make server2
```

Enquanto `server2` estiver parado, ele não é selecionado pelo balanceador.

## Teste de carga

Com o Apache Benchmark instalado, execute:

```bash
make test-load
```

O comando realiza 1.000 requisições com concorrência de 50 clientes contra o balanceador.
