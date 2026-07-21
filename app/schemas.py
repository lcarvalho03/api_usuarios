"""Módulo de esquemas de validação e contratos de dados (DTOs).

Utiliza o Pydantic para estruturar, validar e tipar os dados que entram
e saem das rotas da API, isolando as regras do banco de dados da camada HTTP.
"""

from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator  # <--- Importe 'field_validator'


class UsuarioBase(BaseModel):
    """Esquema base com os campos comuns compartilhados para Usuários."""

    nome: str = Field(..., min_length=3, max_length=50)
    sobre_nome: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    data_nascimento: Optional[date] = None

    @field_validator("data_nascimento")
    @classmethod
    def validar_data_nascimento(cls, v: Optional[date]) -> Optional[date]:
        """Garante que a data de nascimento não seja posterior à data de hoje."""
        if v is not None and v > date.today():
            raise ValueError("A data de nascimento não pode ser posterior à data de hoje.")
        return v


class UsuarioCreate(UsuarioBase):
    """Contrato de dados exigido para a criação de um novo Usuário.

    Recebe a senha em texto puro para que possa ser tratada e criptografada
    na camada de serviço/repositório.
    """

    senha: str = Field(..., min_length=6, max_length=32)


class UsuarioUpdate(BaseModel):
    """Contrato de dados para atualização parcial ou total dos dados de um Usuário.

    Permite que qualquer campo cadastral seja alterado individualmente. Todos os
    campos são opcionais para possibilitar atualizações parciais (PATCH/PUT) sem
    a obrigatoriedade de reintroduzir os dados não modificados.
    """

    nome: Optional[str] = Field(None, min_length=3, max_length=50)
    sobre_nome: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    data_nascimento: Optional[date] = None
    senha: Optional[str] = Field(None, min_length=6, max_length=32)

    @field_validator("data_nascimento")
    @classmethod
    def validar_data_nascimento(cls, v: Optional[date]) -> Optional[date]:
        """Garante que a nova data de nascimento não seja posterior à data de hoje.

        Args:
            v (Optional[date]): A data fornecida no corpo da requisição.

        Returns:
            Optional[date]: A data validada se for anterior ou igual a hoje.

        Raises:
            ValueError: Se a data informada for uma data futura.
        """
        if v is not None and v > date.today():
            raise ValueError("A data de nascimento não pode ser posterior à data de hoje.")
        return v


class UsuarioResponse(UsuarioBase):
    """Contrato de dados retornado pela API nas respostas HTTP.

    Garante a segurança da aplicação ocultando campos sensíveis como a senha.
    """

    id: int
    eh_ativo: bool
    eh_admin: bool
    criado_em: datetime
    alterado_em: Optional[datetime] = None

    # Configuração para o Pydantic ler os objetos do SQLAlchemy automaticamente
    model_config = {"from_attributes": True}
