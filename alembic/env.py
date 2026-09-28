import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context
from app.core.config import get_settings
from app.core.db import Base


# objeto de configuración de Alembic
config = context.config

# configuración de loggers
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# configuración de modelos
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Ejecuta las migraciones en modo offline.

    Se ejecuta cuando se corre Alembic con el comando:
    `alembic upgrade head --sql`.

    Casos de uso:
    - No se tiene acceso directo a la base de datos.
    - Revisión/auditoría antes de aplicar cambios.
    - Entornos con restricciones de permisos.
    - Generar scripts de migración versionados.
    """
    context.configure(
        url=get_settings().db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"}
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Configura el contexto con una conexión síncrona y corre las migraciones."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Crea un motor asíncrono y asocia una conexión con el contexto."""
    connectable = create_async_engine(
        get_settings().db_url,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Ejecuta las migraciones en modo online.

    Se ejecuta cuando se corre Alembic de forma normal, por ejemplo:
    `alembic upgrade head`.

    Casos de uso:
    - Flujo estándar de desarrollo/despliegue, aplicando las
      migraciones directamente contra la base de datos.
    """
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
