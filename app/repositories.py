"""Módulo de repositório de dados do domínio de usuários.

Aplica o padrão Repository para encapsular as consultas e operações de
persistência no banco de dados com SQLAlchemy, isolando a camada HTTP.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Usuario
from app.schemas import UsuarioCreate


class UsuarioRepository:
    """Encapsula as operações de banco de dados para a entidade Usuario."""

    def __init__(self, db: Session) -> None:
        """Inicializa o repositório com a sessão ativa do banco de dados.

        Args:
            db (Session): Sessão ativa do SQLAlchemy.
        """
        self.db = db

    def get_by_id(self, usuario_id: int) -> Optional[Usuario]:
        """Busca um usuário no banco de dados pelo seu ID primário.

        Args:
            usuario_id (int): Identificador único do usuário.

        Returns:
            Optional[Usuario]: O usuário encontrado ou None, caso não exista.
        """
        return self.db.query(Usuario).filter(Usuario.id == usuario_id).first()

    def get_by_email(self, email: str) -> Optional[Usuario]:
        """Busca um usuário no banco de dados pelo seu endereço de e-mail.

        Args:
            email (str): E-mail cadastrado do usuário.

        Returns:
            Optional[Usuario]: O usuário encontrado ou None, caso não exista.
        """
        return self.db.query(Usuario).filter(Usuario.email == email).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Usuario]:
        """Lista usuários cadastrados com suporte a paginação.

        Args:
            skip (int): Quantidade de registros a ignorar (offset).
            limit (int): Limite máximo de registros retornados.

        Returns:
            List[Usuario]: Lista de instâncias da classe Usuario.
        """
        return self.db.query(Usuario).offset(skip).limit(limit).all()

    def create(self, usuario_data: UsuarioCreate, hashed_password: str) -> Usuario:
        """Persiste um novo usuário no banco de dados PostgreSQL.

        Args:
            usuario_data (UsuarioCreate): Dados validados vindos do schema Pydantic.
            hashed_password (str): Senha já criptografada.

        Returns:
            Usuario: A instância do usuário recém-criada e gravada no banco.
        """
        db_usuario = Usuario(
            nome=usuario_data.nome,
            sobre_nome=usuario_data.sobre_nome,
            data_nascimento=usuario_data.data_nascimento,
            email=usuario_data.email,
            hashed_password=hashed_password,
        )
        self.db.add(db_usuario)
        self.db.commit()
        self.db.refresh(db_usuario)
        return db_usuario
