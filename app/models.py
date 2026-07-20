"""Módulo de modelos de dados do domínio da aplicação.

Define as tabelas do banco de dados utilizando o ORM SQLAlchemy,
mapeando as classes Python diretamente para as entidades do PostgreSQL.
"""

from sqlalchemy import Boolean, Column, Date, DateTime, Integer, String
from sqlalchemy.sql import functions
from app.database import Base


class Usuario(Base):
    """Modelo representativo da tabela 'usuarios' no banco de dados.

    Armazena as informações cadastrais, credenciais de acesso e metadados
    de auditoria para o controle de usuários da API.
    """

    __tablename__ = "usuarios"

    id: int = Column(Integer, primary_key=True, index=True)
    nome: str = Column(String(50), nullable=False)
    sobre_nome: str = Column(String(50), nullable=False)
    data_nascimento: Date = Column(Date, nullable=True)
    email: str = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password: str = Column(String(255), nullable=False)
    eh_ativo: bool = Column(Boolean, default=True, nullable=False)
    eh_admin: bool = Column(Boolean, default=False, nullable=False)

    # Metadados de auditoria técnica utilizando a classe de funções explícita
    criado_em = Column(
        DateTime(timezone=True),
        server_default=functions.current_timestamp(),
        nullable=False,
    )

    alterado_em = Column(
        DateTime(timezone=True),
        server_default=functions.current_timestamp(),
        onupdate=functions.current_timestamp(),
        nullable=False,
    )
