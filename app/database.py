"""Módulo de persistência e conexão com o banco de dados.

Configura a engine do SQLAlchemy para comunicação com o PostgreSQL
e fornece a sessão do banco via Injeção de Dependência.
"""

from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from app.config import settings

# Cria o motor de conexão com o banco PostgreSQL
engine = create_engine(settings.DATABASE_URL)

# Fábrica de sessões isoladas por requisição HTTP
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base para o mapeamento das tabelas (ORM)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Abre e fecha uma sessão do banco de dados para cada requisição.

    Yields:
        Generator[Session, None, None]: Instância de sessão ativa do SQLAlchemy.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
