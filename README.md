# API Usuários — User Management REST API

A REST API for user management, built with **FastAPI** and **PostgreSQL**, featuring secure authentication and a fully versioned database schema.

## Features

- User registration and management
- JWT-based authentication
- Password hashing with bcrypt
- Database schema versioning with Alembic migrations
- Data validation with Pydantic

## Tech Stack

- **FastAPI** — web framework for building the API
- **SQLAlchemy 2.0** — ORM for database access
- **Alembic** — database migration management
- **PostgreSQL** (via `psycopg2-binary`) — relational database
- **Pydantic / pydantic-settings** — data validation and configuration management
- **python-jose** — JWT token creation and validation
- **passlib / bcrypt** — secure password hashing
- **Uvicorn** — ASGI server

## Getting Started

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

## Project Structure

```
api_usuarios/
├── alembic/           # Database migration scripts
├── app/                # Application source code
├── .env.example        # Example environment variables
├── alembic.ini          # Alembic configuration
└── requirements.txt      # Python dependencies
```

## What I Learned

Building this project helped me deepen my understanding of REST API design with FastAPI, secure authentication flows with JWT, and managing evolving database schemas with Alembic migrations in a PostgreSQL environment.

---

*Developed as part of my continued studies in Python backend development.*
