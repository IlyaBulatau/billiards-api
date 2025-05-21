"""
Конфигурация соединения с базой данных, проверка на ActivationScope для совестимости с DI инструментом
"""

from rodi import ActivationScope
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from infrastructure.database.context import CURRENT_ASYNC_SESSION
from settings import Settings


def get_async_engine(settings: Settings | ActivationScope) -> AsyncEngine:
    if isinstance(settings, ActivationScope):
        settings = settings.provider.get("settings")

    return create_async_engine(
        settings.database.url,
        future=True,
        max_overflow=settings.database.overflow,
        pool_size=settings.database.pool_size,
        pool_timeout=settings.database.pool_timeout,
        echo=settings.database.echo,
    )


def get_async_session_factory(
    async_engine: AsyncEngine | ActivationScope,
) -> async_sessionmaker[AsyncSession]:
    if isinstance(async_engine, ActivationScope):
        async_engine = async_engine.provider.get("async_engine")

    return async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


def get_async_session(
    async_session_factory: async_sessionmaker[AsyncSession] | ActivationScope,
) -> AsyncSession:
    if isinstance(async_session_factory, ActivationScope):
        async_session_factory = async_session_factory.provider.get("async_session_factory")

    async_session = async_session_factory()
    CURRENT_ASYNC_SESSION.set(async_session)

    return async_session
