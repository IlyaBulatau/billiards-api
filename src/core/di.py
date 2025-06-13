"""
Содержит настройку IoC-контейнеров, которые реализуют DI.
"""

from aioboto3 import Session
from rodi import Container
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from app.billiard.queries.get_club_detail import BilliardClubDetailQuery
from app.billiard.queries.get_clubs import BilliardClubListQuery
from app.booking.commands.reservation_table import ReservationTableCommand
from core.interfaces.commands.bookings import IReservationTableCommand
from core.interfaces.queries.billiards import IBilliardClubDetailQuery, IBilliardClubListQuery
from core.interfaces.repositories import (
    IBilliardClubRepository,
    IBilliardTableRepository,
    IBookingTableRepository,
)
from core.interfaces.storages.s3 import IS3Storage
from infrastructure.database.connections import (
    get_async_engine,
    get_async_session,
    get_async_session_factory,
)
from infrastructure.repositories import (
    BilliarClubRepository,
    BilliarTableRepository,
    BookingTableRepository,
)
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
    container.add_transient(IBookingTableRepository, BookingTableRepository)

    # s3 storage
    container.add_singleton_by_factory(get_s3_session, Session)
    container.add_scoped(IS3Storage, S3Storage)

    # queries
    container.add_transient(IBilliardClubDetailQuery, BilliardClubDetailQuery)
    container.add_transient(IBilliardClubListQuery, BilliardClubListQuery)

    # commands
    container.add_transient(IReservationTableCommand, ReservationTableCommand)

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
            "booking_table_repository": IBookingTableRepository,
            "billiard_club_list_query": IBilliardClubListQuery,
            "billiard_club_detail_query": IBilliardClubDetailQuery,
            "reservation_command": IReservationTableCommand,
        },
        override=True,
    )
