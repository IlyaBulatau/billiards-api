from datetime import datetime, timedelta
import logging
from typing import NoReturn

from essentials.exceptions import NotImplementedException

from core.enums import get_day_of_week_by_int
from core.exceptions.schedules import ClubDoesNotWorkError
from core.utils.datetime_utils import build_dt, get_previous_day
from infrastructure.database.models.billiards import BilliardClub
from infrastructure.database.models.schedules import ClubSchedule


logger = logging.getLogger(__name__)


class ClubScheduleAvailableValidator:
    """Проверка работает ли клуб на опреледенную дату и время"""

    async def validate(self, billiard_club: BilliardClub, target_dt: datetime) -> None:
        """
        Получение расписания предидущего дня и проверка работает ли клуб
        в этом день, проверка попадает ли время для валидации
        в промежуток работы клуба.

        Если не подошло расписание предидущего дня проверить то же самое на текущий
        с учетом того что расписание текущего дня так же может затрагивать 2 дня.

        :param billiard_club: Бильярдный клуба
        :param target_dt: Дата и время на которое нужно проверить расписание клуба
        """

        prev_day_schedule = self._get_schedule_on_day(
            billiard_club, get_previous_day(target_dt).weekday()
        )

        if (
            prev_day_schedule.is_overnight and not prev_day_schedule.is_closed
        ) and self._affects_work_time_prev_day(target_dt, prev_day_schedule):
            return

        today_schedule = self._get_schedule_on_day(billiard_club, target_dt.weekday())

        if self._affects_work_time(target_dt, today_schedule):
            return

        raise ClubDoesNotWorkError

    def _affects_work_time(self, target_dt: datetime, schedule: ClubSchedule) -> bool:
        """Затрагивает ли текущее время время работы клуба текущего дня

        :param target_dt: Дата и время текущее
        :param schedule: Расписание на сегодня
        """

        if not schedule.is_overnight:
            return schedule.opening_time <= target_dt.timetz() <= schedule.closing_time

        schedule_opening = build_dt(target_dt.date(), schedule.opening_time)
        schedule_closing = build_dt((target_dt + timedelta(days=1)).date(), schedule.closing_time)

        return schedule_opening <= target_dt <= schedule_closing

    def _affects_work_time_prev_day(self, target_dt: datetime, schedule: ClubSchedule) -> bool:
        """Затрагивает ли текущее время время работы клуба предидущего дня

        :param target_dt: Дата и время текущее
        :param schedule: Вчерашнее расписание
        """
        schedule_closing_dt = build_dt(target_dt.date(), schedule.closing_time)

        return target_dt <= schedule_closing_dt

    def _get_schedule_on_day(
        self, billiard_club: BilliardClub, weekday: int
    ) -> ClubSchedule | NoReturn:
        """получить расписание работы клуба на определенный день недели

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
