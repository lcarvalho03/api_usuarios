"""Módulo de utilitários de segurança e criptografia.

Fornece funções para geração e verificação de hashes de senhas
utilizando o algoritmo bcrypt através da biblioteca passlib.
"""

from passlib.context import CryptContext

# Configura o contexto de criptografia definindo o bcrypt como algoritmo principal
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(senha: str, senha_hashed: str) -> bool:
    """Verifica se uma senha em texto puro corresponde ao hash armazenado.

    Args:
        senha (str): Senha em texto puro fornecida pelo usuário no login.
        senha_hashed (str): Hash da senha armazenado no banco de dados.

    Returns:
        bool: True se a senha for válida, False caso contrário.
    """
    senha_bytes = senha.encode("utf-8")
    senha_truncada = senha_bytes[:72].decode("utf-8", errors="ignore")
    return pwd_context.verify(senha_truncada, senha_hashed)


def get_password_hash(senha: str) -> str:
    """Gera o hash criptográfico de uma senha em texto puro.

    Args:
        senha (str): Senha enviada pelo usuário em texto puro.

    Returns:
        str: Hash seguro gerado para ser armazenado no banco de dados.
    """
    # 1. Converte a string para bytes em UTF-8
    senha_bytes = senha.encode("utf-8")

    # 2. Trunca os bytes para o limite máximo de 72 bytes do bcrypt
    senha_truncada = senha_bytes[:72].decode("utf-8", errors="ignore")

    # 3. Gera e retorna o hash seguro
    return pwd_context.hash(senha_truncada)
