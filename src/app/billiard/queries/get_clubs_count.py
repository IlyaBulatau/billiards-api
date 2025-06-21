from app.billiard.filters import BilliardClubFilter
from core.interfaces.queries.billiards import IBilliardClubCountQuery
from infrastructure.database.models.billiards import BilliardClub


class BilliardClubCountQuery(IBilliardClubCountQuery[BilliardClub, BilliardClubFilter]):
    async def query(self, filters: BilliardClubFilter) -> int:
        return await self._billiard_club_repository.count(filters)
