# TDE-04 - ShopNow Load Balancer

Balanceador de carga em Python para três instâncias da ShopNow.

## Recursos

- Três instâncias independentes do site (`server1`, `server2` e `server3`);
- Health check HTTP em cada requisição;
- Algoritmos Round Robin e Random;
- Proxy HTTP: o cliente acessa somente o balanceador;
- Simulação de falha de instâncias com Docker Compose.
- Dashboard em tempo real com SSE para comparar os algoritmos.

## Organização do balanceador

Cada módulo tem uma responsabilidade única, sem fragmentar excessivamente o projeto:

- `app.py`: recebe a requisição HTTP, coordena os demais módulos e encaminha a chamada;
- `servers.py`: define as instâncias monitoradas;
- `health_check.py`: verifica a disponibilidade das instâncias;
- `algorithms.py`: escolhe uma instância por Round Robin ou Random;

## Execução

```bash
make up
curl http://localhost:3001/
```

O algoritmo padrão é Round Robin. Para selecionar o aleatório, use:

```bash
curl 'http://localhost:3001/?algorithm=random'
```

O endpoint `http://localhost:3001/health` mostra quais instâncias estão disponíveis.

## Dashboard em tempo real

Abra `http://localhost:3001/dashboard`. Os botões Round Robin e Random geram requisições reais ao balanceador e mostram a distribuição entre as instâncias. Em outro terminal, use `make logs` para acompanhar as mesmas requisições.

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
