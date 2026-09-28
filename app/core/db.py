from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import get_settings

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)


engine = create_async_engine(get_settings().db_url) # motor asíncrono de conexión
SessionLocal = async_sessionmaker(engine, expire_on_commit=False) # fábrica de sesiones asíncronas de base de datos


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Provee una sesión de base de datos para inyectar como dependencia.

    Crea una sesión nueva por request usando `SessionLocal`,
    la entrega con `yield` mientras un endpoint la usa, y al terminar
    (incluso si hubo una excepción) el `async with` se encarga de
    cerrarla automáticamente.
    """
    async with SessionLocal() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]
