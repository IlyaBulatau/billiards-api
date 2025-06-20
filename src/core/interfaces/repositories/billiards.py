from uuid import UUID

from core.interfaces.repositories.abstract import IRepository
from infrastructure.database.models import BilliardClub, BilliardTable


class IBilliardClubRepository(IRepository[BilliardClub]):
    async def get_by_id(self, billiard_club_id: UUID) -> BilliardClub | None:
        """Получить бильярдный клуб по ID"""

    async def count(self) -> int:
        """Получить количество бильярдных клубов"""


class IBilliardTableRepository(IRepository[BilliardTable]):
    async def get_by_id_with_club_and_schedules(
        self, billiard_table_id: UUID
    ) -> BilliardTable | None:
        """Получить бильярдный стол с данными клуба и расписанием"""
