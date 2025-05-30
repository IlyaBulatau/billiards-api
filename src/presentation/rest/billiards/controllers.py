from blacksheep import Response
from blacksheep.server.controllers import get

from app.billiard.filters import BilliardClubFilter
from core.docs import open_api
from core.interfaces.services import IBilliardClubService
from core.schemes import Pagination
from presentation.rest.api_controller import APIController
from presentation.rest.billiards import docs
from settings import Settings


class BilliardClubAPIController(APIController):
    settings: Settings

    @classmethod
    def version(cls) -> str:
        return cls.settings.api_version

    @classmethod
    def route(cls) -> str | None:
        return "/billiard-clubs/"

    @open_api(docs.get_billiard_clubs)
    @get()
    async def get_billiard_clubs(
        self,
        billiard_club_service: IBilliardClubService,
        pagination: Pagination,
        filters: BilliardClubFilter,
    ) -> Response:
        billiard_clubs = await billiard_club_service.get_all(filters, pagination)

        return self.json(data=billiard_clubs)
