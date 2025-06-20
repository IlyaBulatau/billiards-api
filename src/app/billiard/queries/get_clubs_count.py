from core.interfaces.queries.billiards import IBilliardClubCountQuery
from infrastructure.database.models.billiards import BilliardClub


class BilliardClubCountQuery(IBilliardClubCountQuery[BilliardClub]):
    async def query(self) -> int:
        return await self._billiard_club_repository.count()
