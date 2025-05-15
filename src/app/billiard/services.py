from typing import Sequence

from app.billiard.filters import BilliardClubFilter
from app.billiard.schemes.response import BilliardClubAllItemScheme
from core.interfaces.services import IBilliardClubService
from core.schemes.paginations import Pagination
from infrastructure.database.models.billiards import BilliardClub


class BilliardClubService(IBilliardClubService[BilliardClub, BilliardClubFilter]):
    async def get_all(
        self, filters: BilliardClubFilter, pagination: Pagination
    ) -> Sequence[BilliardClubAllItemScheme]:
        billiard_clubs = await self._billiard_club_repository.get_all(filters, pagination)

        return [
            BilliardClubAllItemScheme.model_validate(billiard_club)
            for billiard_club in billiard_clubs
        ]
