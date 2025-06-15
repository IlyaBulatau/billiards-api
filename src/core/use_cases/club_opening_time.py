from datetime import datetime, timedelta

from core.utils.arrays import cyclic_iteration
from core.utils.datetime_utils import build_dt
from infrastructure.database.models.billiards import BilliardClub
from settings import TIMEZONE


def get_nearest_opening_time(billiard_club: BilliardClub) -> datetime | None:
    """
    Получить ближайшее время открытия клуба, подразумиватся что в данный момент клуб не работает.

    Отсортировать список расписаний по текущему дню и пройтись по каждому
    смотря работает ли клуб в этот день и проверяя что время начала работы меньше текущего времени
    """

    current_dt = datetime.now(tz=TIMEZONE)
    loop_dt = current_dt

    day_of_week = current_dt.weekday()

    sorted_schedule = cyclic_iteration(billiard_club.schedules, day_of_week)

    for index, schedule in enumerate(sorted_schedule):
        loop_dt = loop_dt + timedelta(days=index)

        if not schedule.is_closed:
            opening_dt = build_dt(loop_dt.date(), schedule.opening_time)

            if current_dt < opening_dt:
                return opening_dt

    return None
