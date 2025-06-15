import logging
from typing import NoReturn

from essentials.exceptions import NotImplementedException

from core.enums import get_day_of_week_by_int
from infrastructure.database.models.billiards import BilliardClub
from infrastructure.database.models.schedules import ClubSchedule


logger = logging.getLogger(__name__)


def get_schedule_on_day(billiard_club: BilliardClub, weekday: int) -> ClubSchedule | NoReturn:
    """Получить расписание работы клуба на определенный день недели

    :param billiard_club: Бильярдный клуб
    :param weekday: День недели
    """

    day_of_week = get_day_of_week_by_int(weekday)

    try:
        return next(
            schedule
            for schedule in billiard_club.schedules
            if schedule.day_of_week.name == day_of_week
        )
    except StopIteration:
        logger.error(f"Для клуба {billiard_club.id} отсутствует расписание на {day_of_week}")
        raise NotImplementedException
