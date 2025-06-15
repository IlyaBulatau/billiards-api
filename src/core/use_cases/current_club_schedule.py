from datetime import datetime

from core.use_cases.billiard_schedule_on_day import get_schedule_on_day
from core.use_cases.schedule_commons import affects_work_time, affects_work_time_prev_day
from core.utils.datetime_utils import get_previous_day
from infrastructure.database.models.billiards import BilliardClub
from infrastructure.database.models.schedules import ClubSchedule
from settings import TIMEZONE


def get_current_club_schedule(billiard_club: BilliardClub) -> ClubSchedule | None:
    """Получить расписание по которому клуб работает в данный момент времени

    :param billiard_club: Бильярдный клуба
    :return ClubSchedule | None: Расписание или None
    """

    datetime_now = datetime.now(tz=TIMEZONE)

    prev_day_schedule = get_schedule_on_day(billiard_club, get_previous_day(datetime_now).weekday())

    if (
        prev_day_schedule.is_overnight and not prev_day_schedule.is_closed
    ) and affects_work_time_prev_day(datetime_now, prev_day_schedule):
        return prev_day_schedule

    today_schedule = get_schedule_on_day(billiard_club, datetime_now.weekday())

    if affects_work_time(datetime_now, today_schedule):
        return today_schedule

    return None
