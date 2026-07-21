"""Módulo de repositório de dados do domínio de usuários.

Aplica o padrão Repository para encapsular as consultas e operações de
persistência no banco de dados com SQLAlchemy, isolando a camada HTTP.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Usuario
from app.schemas import UsuarioCreate, UsuarioUpdate


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

    def update(
        self,
        usuario: Usuario,
        usuario_data: UsuarioUpdate,
        hashed_password: Optional[str] = None,
    ) -> Usuario:
        """Atualiza no banco de dados os atributos modificados de uma entidade Usuario.

        Aplica apenas os campos que foram explicitamente informados no schema de
        atualização, preservando os demais atributos atuais do modelo.

        Args:
            usuario (Usuario): A instância do usuário carregada do banco de dados.
            usuario_data (UsuarioUpdate): Objeto Pydantic com os campos a serem alterados.
            hashed_password (Optional[str], optional): Novo hash da senha caso a senha tenha
                sido alterada. Padrão é None.

        Returns:
            Usuario: A instância do usuário com seus dados atualizados e persistidos.
        """
        update_dict = usuario_data.model_dump(exclude_unset=True)

        if "senha" in update_dict:
            del update_dict["senha"]

        if hashed_password is not None:
            usuario.hashed_password = hashed_password

        for field, value in update_dict.items():
            setattr(usuario, field, value)

        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def delete(self, usuario: Usuario) -> None:
        """Remove permanentemente um registro de usuário do banco de dados PostgreSQL.

        Args:
            usuario (Usuario): A instância da entidade Usuario a ser excluída.
        """
        self.db.delete(usuario)
        self.db.commit()
