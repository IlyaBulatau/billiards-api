"""
Содержит настройку IoC-контейнеров, которые реализуют DI.
"""

from aioboto3 import Session
from rodi import Container
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from app.billiard.services import BilliardClubService
from core.interfaces.repositories import IBilliardClubRepository, IBilliardTableRepository
from core.interfaces.services import IBilliardClubService
from core.interfaces.storages.s3 import IS3Storage
from infrastructure.database.connections import (
    get_async_engine,
    get_async_session,
    get_async_session_factory,
)
from infrastructure.repositories import BilliarClubRepository, BilliarTableRepository
from infrastructure.storages.s3.client import S3Storage
from infrastructure.storages.s3.s3_session import get_s3_session
from settings import Settings


def configure_di(container: Container, settings: Settings) -> None:
    # settings
    container.add_instance(settings, Settings)

    # connections databse
    container.add_singleton_by_factory(get_async_engine, AsyncEngine)
    container.add_singleton_by_factory(get_async_session_factory, async_sessionmaker[AsyncSession])
    container.add_scoped_by_factory(get_async_session, AsyncSession)

    # repositories
    container.add_transient(IBilliardClubRepository, BilliarClubRepository)
    container.add_transient(IBilliardTableRepository, BilliarTableRepository)

    # s3 storage
    container.add_scoped_by_factory(get_s3_session, Session)
    container.add_transient(IS3Storage, S3Storage)

    # services
    container.add_transient(IBilliardClubService, BilliardClubService)

    # aliases
    container.set_aliases(
        {
            "settings": Settings,
            "async_engine": AsyncEngine,
            "async_session_factory": async_sessionmaker[AsyncSession],
            "async_session": AsyncSession,
            "s3_session": Session,
            "s3_storage": IS3Storage,
            "billiard_club_repository": IBilliardClubRepository,
            "billiard_table_repository": IBilliardTableRepository,
            "billiard_club_service": IBilliardClubService,
        },
        override=True,
    )
