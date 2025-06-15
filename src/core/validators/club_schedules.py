from datetime import datetime
import logging

from core.exceptions.schedules import ClubDoesNotWorkError
from core.use_cases.is_work_billiard_club_now import is_work_billiard_club_now
from infrastructure.database.models.billiards import BilliardClub


logger = logging.getLogger(__name__)


class ClubScheduleAvailableValidator:
    """Проверка работает ли клуб на опреледенную дату и время"""

    async def validate(self, billiard_club: BilliardClub, target_dt: datetime) -> None:
        if not is_work_billiard_club_now(billiard_club, target_dt):
            raise ClubDoesNotWorkError
