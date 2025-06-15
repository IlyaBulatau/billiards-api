from uuid import UUID

from blacksheep import Response, get

from app.billiard.filters import BilliardClubFilter
from core.interfaces.queries.billiards import IBilliardClubDetailQuery, IBilliardClubListQuery
from core.schemes import Pagination
from presentation.html.html_view import HTMLView


class BilliardClubView(HTMLView):
    @get()
    async def get_billiard_clubs(
        self,
        billiard_club_list_query: IBilliardClubListQuery,
        pagination: Pagination,
        filters: BilliardClubFilter,
    ) -> Response:
        billiard_clubs = await billiard_club_list_query.query(filters, pagination)

        return await self.view_async("index.jinja", model={"billiard_clubs": billiard_clubs})

    @get("/billiard-clubs/{billiard_club_id}")
    async def get_billiard_club_detail(
        self, billiard_club_id: UUID, billiard_club_detail_query: IBilliardClubDetailQuery
    ) -> Response:
        billiard_club = await billiard_club_detail_query.query(billiard_club_id)

        return await self.view_async("billiards/billiard_card.jinja", model={"club": billiard_club})
