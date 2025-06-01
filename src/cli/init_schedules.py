from datetime import time
import logging

import fire

from core.enums import DayOfWeek
from core.schemes.paginations import Pagination
from infrastructure.database.connections import (
    get_async_engine,
    get_async_session,
    get_async_session_factory,
)
from infrastructure.database.models.schedules import ClubSchedule
from infrastructure.repositories.billiards import BilliarClubRepository
from infrastructure.repositories.schedules import ClubScheduleRepository
from settings import settings


logger = logging.getLogger()


async def init_schedules() -> None:
    """Создание дефолтного расписания для биллиардых клубов."""

    async_engine = get_async_engine(settings)
    async_session_factory = get_async_session_factory(async_engine)
    async_session = get_async_session(async_session_factory)

    async with async_session.begin():
        billiard_repository = BilliarClubRepository(async_session)
        club_schedule_repository = ClubScheduleRepository(async_session)

        billiard_clubs = await billiard_repository.get_all(None, Pagination(offset=0, limit=100))

        for billiard_club in billiard_clubs:
            for enum in DayOfWeek:
                day = enum.name
                club_schedule = ClubSchedule(
                    billiard_club_id=billiard_club.id,
                    day_of_week=day,
                    opening_time=time(hour=9),
                    closing_time=time(hour=21),
                )

                await club_schedule_repository.create(club_schedule)

        await async_session.commit()

    await async_engine.dispose()


if __name__ == "__main__":
    fire.Fire(init_schedules)
