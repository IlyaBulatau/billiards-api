# type: ignore

"""
Содержит настройку IoC-контейнеров, которые реализуют DI.
"""

from blacksheep import Application
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from app.billiard.services import BilliardClubService
from core.interfaces.repositories import IBilliardClubRepository, IBilliardTableRepository
from core.interfaces.services import IBilliardClubService
from infrastructure.database.connections import (
    get_async_engine,
    get_async_session,
    get_async_session_factory,
)
from infrastructure.repositories import BilliarClubRepository, BilliarTableRepository
from settings import Settings


def configure_di(app: Application, settings: Settings) -> None:
    # settings
    app.services.add_instance(settings, Settings)

    # connections databse
    app.services.add_singleton_by_factory(get_async_engine, AsyncEngine)
    app.services.add_singleton_by_factory(
        get_async_session_factory, async_sessionmaker[AsyncSession]
    )
    app.services.add_scoped_by_factory(get_async_session, AsyncSession)

    # repositories
    app.services.add_transient(IBilliardClubRepository, BilliarClubRepository)
    app.services.add_transient(IBilliardTableRepository, BilliarTableRepository)

    # services
    app.services.add_transient(IBilliardClubService, BilliardClubService)

    # aliases
    app.services.set_aliases(
        {
            "settings": Settings,
            "async_engine": AsyncEngine,
            "async_session_factory": async_sessionmaker[AsyncSession],
            "async_session": AsyncSession,
            "billiard_club_repository": IBilliardClubRepository,
            "billiard_table_repository": IBilliardTableRepository,
            "billiard_club_service": IBilliardClubService,
        },
        override=True,
    )
