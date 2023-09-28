# Graph Theory Maze

## 📃 Trabalho: Desvendando o Labirinto usando API

API disonível em `http://gtm.delary.dev/`

Documentação:
  - [Swagger](gtm.delary.dev/docs/)
  - [Redoc](gtm.delary.dev/redoc/)

## Sumário

- [🎯 Objetivo](#-Objetivo)
- [📝 Descrição](#-Descrição)
- [👀 Entendimento do Labirinto](#-Entendimento-do-Labirinto)
- [📍 Busca do Caminho](#-Busca-do-Caminho)
- [✅ Validação do Caminho](#-Validação-do-Caminho)
- [👩‍🏫 Apresentação](#-Apresentação)
- [🦄 Avaliação](#-Avaliação)
- [🤩 Dicas](#-Dicas)
- [🏗️ Como Rodar o Projeto Localmente?](#-Como-Rodar-o-Projeto-Localmente?)
- [🚀 Como Rodar o Projeto em Produção?](#-Como-Rodar-o-Projeto-em-Produção?)


## 🎯 Objetivo

O objetivo deste trabalho é desenvolver uma ferramenta capaz de decifrar a estrutura de um labirinto representado como um grafo.

Uma vez entendido o labirinto, você deve sugerir a sequência de movimentos otimizada para sair do labirinto a partir de um ponto inicial.

## 📝 Descrição

O labirinto é representado por um grafo onde cada vértice é um ponto que pode ser visitado pelo usuário. Para ajudá-lo a entender e navegar pelo labirinto, você terá acesso a uma API com três endpoints:

### /iniciar:

Permite ao usuário iniciar a exploração do labirinto.

#### Requisição:

```json
{
  "id": "usuario",
  "labirinto": "nome_do_labirinto"
}
```

#### Resposta:

```json
{
    "pos_atual": 5,
    "inicio": true,
    "final": false,
    "movimentos": [4, 6]
}
```


### /movimentar:

Permite ao usuário se mover pelo labirinto.

#### Requisição:

```json
{
  "id": "usuario",
  "labirinto": "nome_do_labirinto",
  "nova_posicao": 6
}
```

#### Resposta:

```json
{
  "pos_atual": 6,
  "inicio": false,
  "final": false,
  "movimentos": [5, 7]
}
```

### /valida_caminho:

Valida se a sequência de movimentos fornecida é um caminho válido no labirinto.

#### Requisição:

```json
{
  "id": "usuario",
  "labirinto": "nome_do_labirinto",
  "todos_movimentos": [5, 6, 7]
}
```

#### Resposta:

```json
{
  "caminho_valido": true,
  "quantidade_movimentos": 3
}
```

## Instruções:

### 👀 Entendimento do Labirinto

Utilize a API fornecida para entender o grafo que representa o labirinto. Seu código deve ser capaz de identificar todos os vértices e arestas.

### 📍 Busca do Caminho

Após entender a estrutura do labirinto, desenvolva um algoritmo que encontre o caminho mais curto (se existir) do ponto inicial até o ponto final.

### ✅ Validação do Caminho

Use o endpoint **/valida_caminho** para confirmar se o caminho encontrado é válido.

### 👩‍🏫 Apresentação

Desenvolva uma interface simples (ou utilize a saída padrão do console) para mostrar a sequência de movimentos que o usuário deve realizar para sair do labirinto.

### 🦄 Avaliação

O trabalho será avaliado com base na acurácia do algoritmo (se ele realmente encontra o melhor caminho), na clareza do código e na apresentação dos resultados.

### 🤩 Dicas

Você pode usar algoritmos de busca em grafos, como o Dijkstra ou o BFS (Busca em Largura), para encontrar o caminho mais curto no labirinto.

Organize bem seu código, separando responsabilidades e documentando as funções.

Não esqueça de tratar possíveis erros que podem surgir durante as chamadas da API.


# 🏗️ Como Rodar o Projeto Localmente?

## 🐳 Docker-Compose

⚠️ Para rodar o projeto utilizando o `docker-compose` é necessário ter o [Docker](https://docs.docker.com/get-docker/) e o [Docker Compose](https://docs.docker.com/compose/install/) instalados.

1. Clone o projeto em uma pasta de sua preferência: `git clone git@github.com:rambim/graph_theory_maze.git`
2. Entre na pasta do repositório que acabou de clonar: `cd graph_theory_maze`
3. Execute o comando: `docker-compose -f docker-compose.yaml -f docker-compose.local.yaml up`

A API estará disponível em (localhost/) e a documentação pode ser consultada em (localhost/docs) e (localhost/redoc).

## 🐍 Python

Para rodar o projeto apenas utilizando o Python, é necessário já ter uma instância do [Redis](https://redis.io/docs/getting-started/) com [RediGraph](https://github.com/RedisGraph/RedisGraph) configurado e rodando. A maneiro mais fácil de subir o Redis com RedisGraph é via docker utilizando a imagem [redislab/redisgraph](https://hub.docker.com/r/redislabs/redisgraph).

Este projeto utiliza o Python 3.11.

1. Clone o projeto em uma pasta de sua preferência: `git clone git@github.com:rambim/graph_theory_maze.git`
2. Entre na pasta do repositório que acabou de clonar: `cd graph_theory_maze`
3. Crie um ambiente virtual: `python -m venv .venv`
4. Ative o ambiente virtual:
  - Linux (Bash ou Zsh): `source ./venv/bin/activate`
  - Windows (Powershell): `.venv\Scripts\Activate.ps1`
5. Instale as dependências: `pip install -r requirements.txt`
6. Configure as variáveis de ambiente com os dados da sua instância do Redis com RediGraph:
  - `export GTM_REDIS_HOST=127.0.0.1`
  - `export GTM_REDIS_PORT=6379`
7. Para rodar a API, execute: `uvicorn api.main:api --host localhost --port 8080`

A API estará disponível em (localhost:8080/) e a documentação pode ser consultada em (localhost:8080/docs) e (localhost:8080/redoc).

# 🚀 Como Rodar o Projeto em Produção?

Antes de efetuar deploy em produção, é necessário adquirir certificado para que a comunicação com a API seja feita tanto em HTTP e HTTPS, principalmente para exposição das documentações (Swagger e Redoc), pois, a depender do domínio, só é possível acessá-lo no *browser* via HTTPS.

Leia mais:
  - [HSTS](https://https.cio.gov/hsts/)
  - [Preloaded HSTS](https://hstspreload.org/)
  - [Let's Encrypt](https://letsencrypt.org/getting-started/)

Após obter os certificados de forma manual, eles devem estar em `./traefik/pki` com os nomes `cert.pem` e `privkey.key`.

O próximo passo é configurar as variáveis de ambiente antes de subir a aplicação:
  - `GTM_DASH_SUBDOMAIN`: Subdomínio do Dashboard do Traefik, exemplo: `dashboard`
  - `GTM_API_SUBDOMAIN`: Subdomínio da aplicação em si, exemplo: `gtm`
  - `GTM_BASE_DOMAIN`: Domínio da base da aplicação, exemplo: `delary.dev`

⚠️ Atenção para os subdominíos, pois não podem possuir mais de 1 nível, ou seja, não podem ser `nivel2.nivel1` ou `dashboard.gtm`.

⚠️ Lembre-se que o certificado deve ser um certificado wildcard para ser possível acessar o dashboard e documentação da aplicação pelo *browser*.

Agora basta utilizar o `Docker Compose` para subir a aplicação utilizando o yaml de produção: `docker-compose -f docker-compose.yaml -f docker-compose.prod.yaml up`.