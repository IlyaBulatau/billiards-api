import asyncio
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

        tasks = [self._prepare_photo_url(club) for club in billiard_clubs if club.photo]
        await asyncio.gather(*tasks)

        return [
            BilliardClubAllItemScheme.model_validate(billiard_club)
            for billiard_club in billiard_clubs
        ]

    async def _prepare_photo_url(self, club: BilliardClub) -> None:
        club.photo = await self._s3_storage.get_url(club.photo)
