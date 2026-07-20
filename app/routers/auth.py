"""Módulo de rotas HTTP para cadastro e gestão de usuários.

Define as rotas da API para registro e consulta de usuários,
integrando validação de schemas, criptografia e persistência no PostgreSQL.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories import UsuarioRepository
from app.schemas import UsuarioCreate, UsuarioResponse
from app.security import get_password_hash

# Define o agrupador de rotas com prefixo e tags para a documentação do Swagger
router = APIRouter(prefix="/auth", tags=["Autenticação e Usuários"])


@router.post(
    "/register",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um novo usuário no sistema",
)
def register_user(
    usuario_data: UsuarioCreate, db: Session = Depends(get_db)
) -> UsuarioResponse:
    """Registra um novo usuário no banco de dados.

    Verifica se o e-mail já está em uso, criptografa a senha com bcrypt
    e persiste a nova entidade.
    
    Args:
        usuario_data (UsuarioCreate): Schema Pydantic contendo nome, e-mail e senha.
        db (Session): Sessão ativa do banco de dados injetada via Depends.

    Returns:
        UsusarioResponse: Objeto do usuário recém-criado sem os dados de senha.

    Raises:
        HTTPException: Retorna status 400 Bad Request se o e-mail já existir.
    """
    repository = UsuarioRepository(db)

    # 1. Regra de Negócio: Não permite e-mails duplicados
    usuario_existe = repository.get_by_email(usuario_data.email)
    if usuario_existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um usuário cadastrado com este e-mail.",
        )

    # 2. Criptografa a senha antes de enviar para a camada de persistência
    hashed_password = get_password_hash(usuario_data.senha)

    # 3. Cria e retorna o novo usuário salvo no PostgreSQL
    new_usuario = repository.create(usuario_data, hashed_password)
    return new_usuario


@router.get(
    "/usuarios",
    response_model=List[UsuarioResponse],
    status_code=status.HTTP_200_OK,
    summary="Lista todos os usuários cadastrados",
)
def list_users(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[UsuarioResponse]:
    """Retorna a lista paginada de usuários cadastrados no banco de dados.
    
    Args:
        skip (int, optional): Quantidade de registros a ignorar no offset.
            Padrão é 0.
        limit (int, optional): Quantidade máxima de registros a retornar.
            Padrão é 100.
        db (Session): Sessão ativa do banco de dados injetada via Depends.

    Returns:
        List[UsuarioResponse]: Lista de usuários cadastrados sem os dados de senha.
    """
    repository = UsuarioRepository(db)
    return repository.get_all(skip=skip, limit=limit)
