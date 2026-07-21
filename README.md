# 👤 API Usuários — User Management REST API

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.139-009688)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-database-336791)
![Alembic](https://img.shields.io/badge/Alembic-migrations-6BA81E)

🇧🇷 [Leia em Português](README.pt-br.md) | 🇺🇸 Read in English

A REST API for user management, built with **FastAPI** and **PostgreSQL**, featuring secure authentication and a fully versioned database schema.

## ✨ Features

- 👤 User registration and management
- 🔐 JWT-based authentication
- 🔑 Password hashing with bcrypt
- 🗃️ Database schema versioning with Alembic migrations
- ✅ Data validation with Pydantic

## 🧰 Tech Stack

| Category | Technology |
|---|---|
| Web Framework | **FastAPI** |
| ORM | **SQLAlchemy 2.0** |
| Migrations | **Alembic** |
| Database | **PostgreSQL** (via `psycopg2-binary`) |
| Validation & Config | **Pydantic** / `pydantic-settings` |
| Authentication | **python-jose** (JWT), **passlib** + **bcrypt** |
| Server | **Uvicorn** (ASGI) |

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL running locally or accessible remotely

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/lcarvalho03/api_usuarios.git
   cd api_usuarios
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Linux/Mac
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env` and fill in your configuration (database URL, JWT secret key, etc.):
   ```bash
   cp .env.example .env
   ```

5. Run the database migrations:
   ```bash
   alembic upgrade head
   ```

6. Start the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`, with interactive documentation at `http://localhost:8000/docs` (Swagger UI).

## 📁 Project Structure

```
api_usuarios/
├── alembic/            # Database migration scripts
├── app/                # Application source code
│   ├── routers/        # HTTP Endpoints (FastAPI APIRouter)
│   ├── config.py       # Pydantic Settings environment configuration
│   ├── database.py     # SQLAlchemy engine & session setup
│   ├── models.py       # SQLAlchemy ORM models
│   ├── repositories.py # Repository Pattern (Data access layer)
│   ├── schemas.py      # Pydantic v2 DTOs & validations
│   └── security.py     # Password hashing & security utilities
├── .env.example        # Example environment variables
├── alembic.ini         # Alembic configuration
└── requirements.txt    # Python dependencies
```

## 🛠️ Architecture and Best Practices

This project was developed with a focus on maintainability, readability, and security, applying the following principles:

### 📐 SOLID Principles
- **Single Responsibility Principle (SRP):** clear separation between routing, business logic, and data persistence layers.
- **Dependency Inversion:** FastAPI's dependency injection (`Depends`) is used to decouple route handlers from concrete database sessions and services.

### ♻️ DRY (Don't Repeat Yourself)
- Shared logic (authentication, database session handling, validation schemas) is centralized rather than duplicated across endpoints.

### 🔐 Security
- Passwords are never stored in plain text — hashed with **bcrypt** via `passlib`.
- Authentication handled with signed **JWT** tokens (`python-jose`).
- Sensitive configuration (database credentials, secret keys) kept out of version control via `.env`.

### 🐍 Code Style (PEP 8)
- Standardized naming conventions: `snake_case` for functions/variables, `PascalCase` for classes.
- Data validation and serialization handled declaratively through **Pydantic** models.

## 📚 What I Learned

Building this project helped me deepen my understanding of REST API design with FastAPI, secure authentication flows with JWT, and managing evolving database schemas with Alembic migrations in a PostgreSQL environment.

---

*Developed as part of my continued studies in Python backend development.*
