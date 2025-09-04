# DimDim — Docker Compose (Flask + Postgres)

Projeto mínimo e **100% funcional** para o 1º Checkpoint – 2º Semestre: **Docker Compose** (DevOps Tools & Cloud Computing).

> Requisitos atendidos: dois serviços (app + db) com imagens oficiais, redes internas (padrão do Compose), **volumes** de dados, **variáveis de ambiente** via `.env`, **políticas de restart**, **exposição de portas**, **healthchecks** nos serviços e **usuário sem privilégios** para executar a aplicação.

## Arquitetura (Atual → Futura)

**Atual (antes da conteinerização):**
- App Python/Flask rodando na máquina do desenvolvedor
- Banco Postgres instalado localmente
- Deploy manual, variação entre ambientes

**Futura (com Docker Compose):**
```mermaid
flowchart LR
  subgraph Host
    subgraph Docker_Network
      A[Flask App (Gunicorn)\nporta 8000] -- SQLAlchemy --> B[(Postgres 16-alpine)]
    end
  end
```

## Como rodar

1. **Pré-requisitos**: Docker + Docker Compose plugin
2. Copie o arquivo `.env.example` para `.env` e ajuste, se necessário:
   ```bash
   cp .env.example .env
   ```
3. Build e subida dos serviços:
   ```bash
   docker compose up -d --build
   ```
4. Acesse: <http://localhost:8000>

> O Compose cria uma rede interna para os serviços se comunicarem. O serviço `app` fala com `db` pelo hostname **`db`** (definido no Compose).

## Teste do CRUD (via `curl`)

Criar:
```bash
curl -sS -X POST http://localhost:8000/api/customers \\
  -H "Content-Type: application/json" \\
  -d '{"name":"Ana","email":"ana@example.com"}' | jq
```

Listar:
```bash
curl -sS http://localhost:8000/api/customers | jq
```

Atualizar:
```bash
curl -sS -X PUT http://localhost:8000/api/customers/1 \\
  -H "Content-Type: application/json" \\
  -d '{"name":"Ana Maria"}' | jq
```

Excluir:
```bash
curl -sS -X DELETE http://localhost:8000/api/customers/1 | jq
```

Healthcheck HTTP da app:
```bash
curl -sS http://localhost:8000/health
```

## Detalhes de implementação
- **Imagens oficiais**: `python:3.12-slim` e `postgres:16-alpine`.
- **Usuário sem privilégios**: o container da app cria e roda como `app`.
- **Volumes**: `db-data` persiste os dados do Postgres.
- **Variáveis de ambiente**: `.env` gerencia credenciais e configurações.
- **Healthchecks**: `pg_isready` para DB, `curl` HTTP para a app.
- **Política de restart**: `unless-stopped` nos dois serviços.
- **Exposição de portas**: `8000:8000` (app).

## Comandos essenciais do Docker Compose
```bash
# Subir em background
docker compose up -d

# Build das imagens
docker compose build

# Logs de um serviço
docker compose logs -f app
docker compose logs -f db

# Status e saúde dos containers
docker compose ps

# Reiniciar um serviço
docker compose restart app

# Derrubar tudo (mantendo volume de dados)
docker compose down

# Derrubar e remover volume de dados (CUIDADO: apaga o banco)
docker compose down -v
```

## Troubleshooting
- **A porta 8000 já está em uso**: edite `docker-compose.yml` e altere para `8080:8000` (lado esquerdo).
- **DB demora a ficar “healthy”**: o `depends_on` aguarda o healthcheck do Postgres. Verifique `docker compose logs -f db`.
- **Erro de conexão ao DB**: confirme o `DATABASE_URL` no serviço `app` e as credenciais no `.env`.
- **Pacotes Python**: reconstrua a imagem quando alterar `requirements.txt`: `docker compose build app && docker compose up -d`.

## Roteiro para o vídeo (sugestão)
1. Mostre o repositório: estrutura e `docker-compose.yml`.
2. Copie `.env.example` → `.env`.
3. Rode `docker compose up -d --build`.
4. Mostre `docker compose ps` (saúde de `app` e `db`).
5. Abra `http://localhost:8000` e faça o CRUD na interface.
6. Mostre as chamadas `curl` no terminal.
7. Finalize mostrando logs: `docker compose logs -f app`/`db`.

---
_Gerado em 2025-09-04._
