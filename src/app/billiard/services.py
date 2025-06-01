import asyncio
from typing import NoReturn, Sequence
from uuid import UUID

from essentials.exceptions import ObjectNotFound
from pydantic import BaseModel

from app.billiard.filters import BilliardClubFilter
from app.billiard.schemes.response import BilliardClubAllItemScheme, BilliardClubDetailScheme
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

    async def get_detail(self, billiard_club_id: UUID) -> BilliardClubDetailScheme | NoReturn:
        billiard_club = await self._billiard_club_repository.get_by_id(billiard_club_id)

        if not billiard_club:
            raise ObjectNotFound()

        if billiard_club.phone:
            await self._prepare_photo_url(billiard_club)

        return BilliardClubDetailScheme.model_validate(billiard_club)

    async def _prepare_photo_url(self, club: BilliardClub) -> None:
        club.photo = await self._s3_storage.get_url(club.photo)
