"""Módulo de rotas HTTP para cadastro e gestão de usuários.

Define as rotas da API para registro e consulta de usuários,
integrando validação de schemas, criptografia e persistência no PostgreSQL.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories import UsuarioRepository
from app.schemas import UsuarioCreate, UsuarioResponse, UsuarioUpdate
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


@router.get(
    "/usuarios/by-email",
    response_model=UsuarioResponse,
    status_code=status.HTTP_200_OK,
    summary="Busca um usuário específico pelo seu E-mail",
)
def get_user_by_email(
    email: str, db: Session = Depends(get_db)
) -> UsuarioResponse:
    """Recupera os detalhes cadastrais de um usuário com base no seu E-mail.

    Args:
        email (str): E-mail do usuário no banco de dados.
        db (Session): Sessão ativa do banco de dados injetada via Depends.

    Returns:
        UsuarioResponse: Dados públicos do usuário consultado.

    Raises:
        HTTPException: Retorna status 404 Not Found caso o e-mail não seja encontrado.
    """
    repository = UsuarioRepository(db)
    usuario = repository.get_by_email(email)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado.",
        )
    return usuario


@router.get(
    "/usuarios/{usuario_id}",
    response_model=UsuarioResponse,
    status_code=status.HTTP_200_OK,
    summary="Busca um usuário específico pelo seu ID",
)
def get_user_by_id(
    usuario_id: int, db: Session = Depends(get_db)
) -> UsuarioResponse:
    """Recupera os detalhes cadastrais de um usuário com base no seu ID primário.

    Args:
        usuario_id (int): Identificador único do usuário no banco de dados.
        db (Session): Sessão ativa do banco de dados injetada via Depends.

    Returns:
        UsuarioResponse: Dados públicos do usuário consultado.

    Raises:
        HTTPException: Retorna status 404 Not Found caso o ID não seja encontrado.
    """
    repository = UsuarioRepository(db)
    usuario = repository.get_by_id(usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado.",
        )
    return usuario


@router.put(
    "/usuarios/{usuario_id}",
    response_model=UsuarioResponse,
    status_code=status.HTTP_200_OK,
    summary="Atualiza as informações cadastrais de um usuário",
)
def update_user(
    usuario_id: int,
    usuario_data: UsuarioUpdate,
    db: Session = Depends(get_db),
) -> UsuarioResponse:
    """Atualiza parcialmente ou totalmente os dados de um usuário existente.

    Valida se o usuário existe no banco de dados e impede a alteração do e-mail
    para um endereço que já pertença a outra conta registrada.

    Args:
        usuario_id (int): Identificador único do usuário a ser alterado.
        usuario_data (UsuarioUpdate): Schema Pydantic com os campos a atualizar.
        db (Session): Sessão ativa do banco de dados injetada via Depends.

    Returns:
        UsuarioResponse: Instância do usuário com suas informações atualizadas.

    Raises:
        HTTPException: Retorna status 404 Not Found se o usuário não for encontrado,
            ou status 400 Bad Request se o novo e-mail já estiver cadastrado.
    """
    repository = UsuarioRepository(db)

    usuario = repository.get_by_id(usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado.",
        )

    if usuario_data.email and usuario_data.email != usuario.email:
        email_em_uso = repository.get_by_email(usuario_data.email)
        if email_em_uso:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este e-mail já está em uso por outro usuário.",
            )

    hashed_password = None
    if usuario_data.senha:
        hashed_password = get_password_hash(usuario_data.senha)

    updated_usuario = repository.update(usuario, usuario_data, hashed_password)
    return updated_usuario


@router.delete(
    "/usuarios/{usuario_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Exclui permanentemente um usuário do sistema",
)
def delete_user(usuario_id: int, db: Session = Depends(get_db)) -> None:
    """Remove o registro de um usuário do banco de dados a partir do seu ID.

    Args:
        usuario_id (int): Identificador único do usuário a ser removido.
        db (Session): Sessão ativa do banco de dados injetada via Depends.

    Returns:
        None: Retorna uma resposta com corpo vazio e status 204 No Content.

    Raises:
        HTTPException: Retorna status 404 Not Found se o usuário não existir.
    """
    repository = UsuarioRepository(db)

    usuario = repository.get_by_id(usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado.",
        )

    repository.delete(usuario)
    return None
