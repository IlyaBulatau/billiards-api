from uuid import UUID

from core.interfaces.repositories.abstract import IRepository
from infrastructure.database.models import BilliardClub, BilliardTable


class IBilliardClubRepository(IRepository[BilliardClub]):
    async def get_by_id(self, billiard_club_id: UUID) -> BilliardClub | None: ...


class IBilliardTableRepository(IRepository[BilliardTable]):
    pass
