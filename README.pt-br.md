# 👤 API Usuários — API REST de Gerenciamento de Usuários

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.139-009688)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-database-336791)
![Alembic](https://img.shields.io/badge/Alembic-migrations-6BA81E)

🇧🇷 Leia em Português | 🇺🇸 [Read in English](README.md)

Uma API REST para gerenciamento de usuários, construída com **FastAPI** e **PostgreSQL**, com autenticação segura e versionamento completo do esquema do banco de dados.

## ✨ Funcionalidades

- 👤 Cadastro e gerenciamento de usuários
- 🔐 Autenticação baseada em JWT
- 🔑 Hash de senhas com bcrypt
- 🗃️ Versionamento do esquema do banco de dados com migrações Alembic
- ✅ Validação de dados com Pydantic

## 🧰 Tecnologias Utilizadas

| Categoria | Tecnologia |
|---|---|
| Framework Web | **FastAPI** |
| ORM | **SQLAlchemy 2.0** |
| Migrações | **Alembic** |
| Banco de Dados | **PostgreSQL** (via `psycopg2-binary`) |
| Validação e Configuração | **Pydantic** / `pydantic-settings` |
| Autenticação | **python-jose** (JWT), **passlib** + **bcrypt** |
| Servidor | **Uvicorn** (ASGI) |

## 🚀 Como Começar

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

## 📁 Estrutura do Projeto

```
api_usuarios/
├── alembic/           # Scripts de migração do banco de dados
├── app/                # Código-fonte da aplicação
├── .env.example        # Exemplo de variáveis de ambiente
├── alembic.ini          # Configuração do Alembic
└── requirements.txt      # Dependências do Python
```

## 🛠️ Arquitetura e Boas Práticas

Este projeto foi desenvolvido com foco em manutenibilidade, legibilidade e segurança, aplicando os seguintes princípios:

### 📐 Princípios SOLID
- **Princípio da Responsabilidade Única (SRP):** separação clara entre as camadas de rotas, lógica de negócio e persistência de dados.
- **Inversão de Dependência:** a injeção de dependências do FastAPI (`Depends`) é usada para desacoplar os handlers de rota das sessões de banco de dados e serviços concretos.

### ♻️ DRY (Não se Repita)
- Lógica compartilhada (autenticação, gerenciamento de sessão do banco, esquemas de validação) é centralizada em vez de duplicada entre os endpoints.

### 🔐 Segurança
- Senhas nunca são armazenadas em texto puro — são convertidas em hash com **bcrypt** via `passlib`.
- Autenticação feita com tokens **JWT** assinados (`python-jose`).
- Configurações sensíveis (credenciais do banco, chaves secretas) mantidas fora do controle de versão através do `.env`.

### 🐍 Estilo de Código (PEP 8)
- Convenções de nomenclatura padronizadas: `snake_case` para funções/variáveis, `PascalCase` para classes.
- Validação e serialização de dados feitas de forma declarativa através de modelos **Pydantic**.

## 📚 O que Aprendi

Construir este projeto me ajudou a aprofundar meu entendimento sobre design de APIs REST com FastAPI, fluxos de autenticação segura com JWT, e gerenciamento de esquemas de banco de dados em evolução com migrações Alembic em ambiente PostgreSQL.

---

*Desenvolvido como parte dos meus estudos contínuos em desenvolvimento backend com Python.*
