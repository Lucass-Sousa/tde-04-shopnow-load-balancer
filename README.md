# TDE-04 - ShopNow Load Balancer

Três instâncias da ShopNow em Python, distribuídas por um balanceador de carga Nginx.

## Pré-requisitos

- Docker Engine ou Docker Desktop com Docker Compose;
- `make`;
- Python 3 para os monitores executados no terminal;
- Apache Benchmark (`ab`), instalado com `make install` em sistemas Ubuntu/Debian.

## Execução no Windows

Para manter os mesmos comandos `make`, utilize Docker Desktop com WSL 2 e o terminal Ubuntu integrado ao VS Code.

1. Instale o [Docker Desktop](https://docs.docker.com/desktop/setup/install/windows-install/) e habilite o modo **Linux containers**;
2. Em um PowerShell aberto como administrador, execute `wsl --install` e reinicie o computador quando solicitado;
3. No Docker Desktop, acesse **Settings > General** e habilite **Use WSL 2 based engine**;
4. Em **Settings > Resources > WSL Integration**, habilite a distribuição Ubuntu;
5. No VS Code, instale a extensão WSL e use o comando **WSL: Reopen Folder in WSL**.

No terminal Ubuntu do VS Code, instale as ferramentas necessárias:

```bash
sudo apt update
sudo apt install -y make apache2-utils python3
```

Depois, os comandos do projeto funcionam normalmente:

```bash
make up
make start-round-robin
make test-load-round-robin
```

O navegador do Windows acessa a aplicação em `http://localhost:3001`.

## Recursos

- Três instâncias independentes do site (`server1`, `server2` e `server3`);
- Nginx como proxy reverso e único ponto de entrada;
- Algoritmos Round Robin e Least Connections;
- Desvio passivo de instâncias indisponíveis (`max_fails` e `fail_timeout`);
- Simulação de falha de instâncias com Docker Compose.

## Organização

O arquivo `nginx/nginx.conf` define os dois grupos de servidores:

- `shopnow_round_robin`: algoritmo padrão do Nginx;
- `shopnow_least_connections`: usa a diretiva `least_conn`.

As aplicações em `instancias/app.py` representam os três servidores da loja e retornam o cabeçalho `X-ShopNow-Server`, usado pelos scripts para identificar qual instância atendeu cada requisição.

## Execução

```bash
make install
make up
curl http://localhost:3001/
```

O algoritmo padrão é Round Robin. Para selecionar Least Connections, use:

```bash
curl 'http://localhost:3001/?algorithm=least-conn'
```

O endpoint `http://localhost:3001/health` é encaminhado pelo Nginx para uma instância disponível.

## Acompanhamento pelo terminal

Em um terminal, execute `make logs` para acompanhar os atendimentos das instâncias.

Para enviar e observar uma requisição por vez, use. O terminal exibirá somente o servidor que respondeu:

```bash
make request
make request ALGORITMO=least-conn
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
make start-least-conn
make start-comparacao
```

O arquivo `.env` é obrigatório para `make start`; não há valores padrão para quantidade ou intervalo.

Os dois primeiros comandos atualizam barras no terminal durante a execução, mostrando a distribuição de um algoritmo. O comando `make start-comparacao` envia uma requisição Round Robin e uma Least Connections por ciclo, exibindo as duas distribuições no mesmo painel.

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
make test-load-round-robin
make test-load-least-conn
```

Cada comando realiza 1.000 requisições com concorrência de 50 clientes contra o balanceador, usando o algoritmo indicado. `make test-load` continua disponível como atalho para Round Robin.

O parâmetro `-l` do Apache Benchmark aceita respostas com tamanho variável, pois cada instância inclui seu contador de requisições na resposta.

No resultado, os indicadores principais são:

```text
Complete requests:      1000
Failed requests:        0
Requests per second:    <valor variável>
```

`Complete requests` confirma que as 1.000 requisições foram processadas; `Failed requests: 0` indica que nenhuma falhou. O valor de `Requests per second` varia conforme a máquina utilizada e a carga do sistema.
