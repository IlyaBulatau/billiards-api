from datetime import time
import logging
from typing import NoReturn

from essentials.exceptions import NotImplementedException

from core.use_cases.current_club_schedule import get_current_club_schedule
from infrastructure.database.models.billiards import BilliardClub


logger = logging.getLogger(__name__)


def get_closing_time(billiard_club: BilliardClub) -> time | NoReturn:
    schedule = get_current_club_schedule(billiard_club)

    if not schedule:
        logger.error(
            "Не удалось получить время закрытия клуба, "
            f"в текущий момент клуб не работает. Club ID: {billiard_club.id}"
        )
        raise NotImplementedException

    return schedule.closing_time
