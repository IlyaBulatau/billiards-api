from datetime import datetime, timedelta

from core.utils.datetime_utils import build_dt
from infrastructure.database.models.schedules import ClubSchedule


def affects_work_time(target_dt: datetime, schedule: ClubSchedule) -> bool:
    """Затрагивает ли текущее время время работы клуба текущего дня

    :param target_dt: Дата и время текущее
    :param schedule: Расписание на сегодня
    """

    if not schedule.is_overnight:
        return schedule.opening_time <= target_dt.timetz() <= schedule.closing_time

    schedule_opening = build_dt(target_dt.date(), schedule.opening_time)
    schedule_closing = build_dt((target_dt + timedelta(days=1)).date(), schedule.closing_time)

    return schedule_opening <= target_dt <= schedule_closing


def affects_work_time_prev_day(target_dt: datetime, schedule: ClubSchedule) -> bool:
    """Затрагивает ли текущее время время работы клуба предидущего дня

    :param target_dt: Дата и время текущее
    :param schedule: Вчерашнее расписание
    """
    schedule_closing_dt = build_dt(target_dt.date(), schedule.closing_time)

    return target_dt <= schedule_closing_dt
