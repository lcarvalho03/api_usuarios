"""Módulo de configuração da aplicação.

Carrega e valida as variáveis de ambiente necessárias para a inicialização
da API utilizando as capacidades de tipagem do Pydantic Settings.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Gerencia as variáveis de ambiente e configurações globais da API."""

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Configura o Pydantic para ler o arquivo .env de forma segura
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# Instância global para importação direta nos módulos da aplicação
settings = Settings()
