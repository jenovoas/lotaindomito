"""
Alembic env.py — configuración para migraciones async con SQLAlchemy 2 + asyncpg.

Se usa AsyncEngine para mantener la sesión alembic en modo async.
El URL se inyecta desde settings para no hardcodear credenciales.
"""
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

# Importar Base y modelos para autogenerate
from app.models import Base  # noqa: F401
from app.models.zona import Zona  # noqa: F401

# Config de Alembic
config = context.config

# Configurar log
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadatos para autogenerate
target_metadata = Base.metadata


def get_url() -> str:
    """
    Obtiene DATABASE_URL del entorno o usa default de desarrollo.
    Permite override via alembic.ini [alembic] sqlalchemy.url.
    """
    import os

    db_url = os.environ.get(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5432/lotaindomito",
    )
    return db_url


def run_migrations_offline() -> None:
    """
    Modo offline — genera SQL sin conectar a la DB.
    Útil para pre-visualizar migraciones.
    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Ejecuta migraciones con una conexión synchrone."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    Modo async — usa AsyncEngine para migrar con asyncpg.
    """
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = get_url()

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Entry point — ejecuta migraciones en nuevo event loop."""
    import asyncio
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
