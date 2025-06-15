from typing import NoReturn
from uuid import UUID

from essentials.exceptions import ObjectNotFound

from app.billiard.schemes.response import BilliardClubDetailScheme
from core.interfaces.queries.billiards import IBilliardClubDetailQuery
from infrastructure.database.models.billiards import BilliardClub


class BilliardClubDetailQuery(IBilliardClubDetailQuery[BilliardClub]):
    async def query(self, billiard_club_id: UUID) -> BilliardClubDetailScheme | NoReturn:
        billiard_club = await self._billiard_club_repository.get_by_id(billiard_club_id)

        if not billiard_club:
            raise ObjectNotFound

        if billiard_club.photo:
            await self._prepare_photo_url(billiard_club)

        return BilliardClubDetailScheme.model_validate(
            billiard_club, context={"instance": billiard_club}
        )

    async def _prepare_photo_url(self, club: BilliardClub) -> None:
        club.photo = await self._s3_storage.get_url(club.photo)
