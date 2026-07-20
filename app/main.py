"""Ponto de entrada principal da Task & Analytics API.

Inicializa a instância do FastAPI, configura metadados globais e
expõe as rotas iniciais de verificação de status do sistema.
"""

from typing import Dict
from fastapi import FastAPI
from app.database import Base, engine
import app.models  # Importante para que o SQLAlchemy mapeie o modelo Usuario
from app.routers import auth

# Cria as tabelas no banco de dados (no caso, PostgreSQL) caso ainda não existam
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Tarefas e Análise",
    description="API REST modular para gerenciamento de equipes e indicadores de produtividade.",
    version="1.0.0",
)

# Conecta o módulo de rotas de autenticação e usuários à aplicação principal
app.include_router(auth.router)


@app.get("/", response_model=Dict[str, str])
def read_root() -> Dict[str, str]:
    """Verifica se o servidor está online e respondendo adequadamente.

    Returns:
        Dict[str, str]: Um dicionário com o status atual da aplicação.
    """
    return {
        "status": "Online",
        "message": "API rodando perfeitamente!",
        "documentation": "Acesse /docs para o Swagger interativo.",
    }
