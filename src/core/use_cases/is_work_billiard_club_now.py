from datetime import datetime

from core.use_cases.billiard_schedule_on_day import get_schedule_on_day
from core.use_cases.schedule_commons import affects_work_time, affects_work_time_prev_day
from core.utils.datetime_utils import get_previous_day
from infrastructure.database.models.billiards import BilliardClub


def is_work_billiard_club_now(billiard_club: BilliardClub, target_dt: datetime) -> bool:
    """
    Получение расписания предидущего дня и проверка работает ли клуб
    в этом день, проверка попадает ли время для валидации
    в промежуток работы клуба.

    Если не подошло расписание предидущего дня проверить то же самое на текущий
    с учетом того что расписание текущего дня так же может затрагивать 2 дня.

    :param billiard_club: Бильярдный клуба
    :param target_dt: Дата и время на которое нужно проверить расписание клуба
    """

    prev_day_schedule = get_schedule_on_day(billiard_club, get_previous_day(target_dt).weekday())

    if (
        prev_day_schedule.is_overnight and not prev_day_schedule.is_closed
    ) and affects_work_time_prev_day(target_dt, prev_day_schedule):
        return True

    today_schedule = get_schedule_on_day(billiard_club, target_dt.weekday())

    if affects_work_time(target_dt, today_schedule):  # noqa: SIM103
        return True

    return False
