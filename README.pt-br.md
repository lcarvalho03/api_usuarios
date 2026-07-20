# API Usuários — API REST de Gerenciamento de Usuários

Uma API REST para gerenciamento de usuários, construída com **FastAPI** e **PostgreSQL**, com autenticação segura e versionamento completo do esquema do banco de dados.

## Funcionalidades

- Cadastro e gerenciamento de usuários
- Autenticação baseada em JWT
- Hash de senhas com bcrypt
- Versionamento do esquema do banco de dados com migrações Alembic
- Validação de dados com Pydantic

## Tecnologias Utilizadas

- **FastAPI** — framework web para construção da API
- **SQLAlchemy 2.0** — ORM para acesso ao banco de dados
- **Alembic** — gerenciamento de migrações do banco de dados
- **PostgreSQL** (via `psycopg2-binary`) — banco de dados relacional
- **Pydantic / pydantic-settings** — validação de dados e gerenciamento de configurações
- **python-jose** — criação e validação de tokens JWT
- **passlib / bcrypt** — hash seguro de senhas
- **Uvicorn** — servidor ASGI

## Como Começar

### Pré-requisitos

- Python 3.10+
- PostgreSQL rodando localmente ou acessível remotamente

### Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/lcarvalho03/api_usuarios.git
   cd api_usuarios
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Linux/Mac
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Copie o `.env.example` para `.env` e preencha as configurações (URL do banco de dados, chave secreta do JWT, etc.):
   ```bash
   cp .env.example .env
   ```

5. Execute as migrações do banco de dados:
   ```bash
   alembic upgrade head
   ```

6. Inicie o servidor de desenvolvimento:
   ```bash
   uvicorn app.main:app --reload
   ```

A API ficará disponível em `http://localhost:8000`, com documentação interativa em `http://localhost:8000/docs` (Swagger UI).

## Estrutura do Projeto

```
api_usuarios/
├── alembic/           # Scripts de migração do banco de dados
├── app/                # Código-fonte da aplicação
├── .env.example        # Exemplo de variáveis de ambiente
├── alembic.ini          # Configuração do Alembic
└── requirements.txt      # Dependências do Python
```

## O que Aprendi

Construir este projeto me ajudou a aprofundar meu entendimento sobre design de APIs REST com FastAPI, fluxos de autenticação segura com JWT, e gerenciamento de esquemas de banco de dados em evolução com migrações Alembic em ambiente PostgreSQL.

---

*Desenvolvido como parte dos meus estudos contínuos em desenvolvimento backend com Python.*
