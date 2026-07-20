"""Módulo de configuração do ambiente de migrações do Alembic.

Este arquivo é responsável por carregar o contexto de execução das migrações,
configurar o motor de banco de dados SQLAlchemy dinamicamente a partir das
configurações da aplicação (`app.config.settings`) e registrar os metadados dos
modelos (`app.database.Base`) para a geração automática de migrações (autogenerate).
"""

# pylint: disable=no-member
# O Pylint não consegue inferir os atributos de `alembic.context`, pois ele é
# montado dinamicamente em tempo de execução via um objeto proxy interno do
# Alembic. Isso é um falso positivo conhecido, já mitigado para o Pyright
# através da anotação `context: Any` logo abaixo.

import sys
from logging.config import fileConfig
from pathlib import Path
from typing import Any

from sqlalchemy import engine_from_config, pool
import alembic.context as alembic_context

# 1. Garante que a raiz do projeto esteja no PYTHONPATH antes de importar a 'app'
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# 2. Imports da aplicação (após sys.path para funcionar em tempo de execução)
# pylint: disable=wrong-import-position
from app.config import settings  # pyright: ignore[reportImportsFromNotAtTop]  # noqa: E402
from app.database import Base  # pyright: ignore[reportImportsFromNotAtTop]  # noqa: E402
# pylint: disable-next=unused-import
import app.models  # type: ignore  # noqa: F401, E402
# pylint: enable=wrong-import-position

# Tratamento do contexto dinâmico do Alembic para o analisador estático
context: Any = alembic_context

# Objeto de configuração do Alembic provido pelo arquivo alembic.ini
config = context.config

# Define a URL de conexão recuperada das variáveis de ambiente da aplicação
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Configura o manipulador de logs padrão do Python se um arquivo .ini for fornecido
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Define o objeto Metadata contendo a estrutura dos modelos declarados no SQLAlchemy
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Executa as migrações do banco de dados no modo 'offline'.

    Neste modo, o Alembic não estabelece uma conexão direta com o banco de
    dados. Ele apenas compila as instruções SQL geradas e as exibe na saída
    padrão ou as salva em um arquivo de script.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Executa as migrações do banco de dados no modo 'online'.

    Cria uma engine de conexão com o banco de dados PostgreSQL utilizando as
    configurações da aplicação e aplica as alterações diretamente dentro de
    uma transação ativa.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# Executa o fluxo apropriado dependendo de como a CLI do Alembic foi invocada
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
