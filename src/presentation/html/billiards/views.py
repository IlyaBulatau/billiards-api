import asyncio
from typing import Any
from uuid import UUID

from blacksheep import Request, Response, get

from app.billiard.filters import BilliardClubFilter
from core.interfaces.queries.billiards import (
    IBilliardClubCountQuery,
    IBilliardClubDetailQuery,
    IBilliardClubListQuery,
)
from core.schemes import Pagination
from presentation.html.html_view import HTMLView


class BilliardClubView(HTMLView):
    @get()
    async def index(
        self,
        billiard_club_list_query: IBilliardClubListQuery,
        pagination: Pagination,
        filters: BilliardClubFilter,
    ) -> Response:
        """Главная страница со списком самых популярных клубов"""

        billiard_clubs = await billiard_club_list_query.query(filters, pagination)

        return await self.view_async("index.jinja", model={"billiard_clubs": billiard_clubs})

    @get("/billiard-clubs/")
    async def get_billiard_clubs(
        self,
        request: Request,
        billiard_club_list_query: IBilliardClubListQuery,
        billiard_club_count_query: IBilliardClubCountQuery,
        pagination: Pagination,
        filters: BilliardClubFilter,
    ) -> Response:
        """Страница со всеми клубами с фильтрацией и пагинацией"""

        billiard_clubs, total_count = await asyncio.gather(
            billiard_club_list_query.query(filters, pagination),
            billiard_club_count_query.query(filters),
        )

        filter_dict = filters.model_dump(exclude_none=True, exclude_unset=True)

        context: dict[str, Any] = {
            "total_count": total_count,
            "limit": pagination.limit,
            "offset": pagination.offset,
            "page": pagination.page or 1,
            "url": "billiard-clubs",
            "request": request,
            # для сохранения фильтров при пагинации
            "filters_query": "&".join([f"{k}={v}" for k, v in filter_dict.items()]),
            **filter_dict,
        }

        return await self.view_async(
            "billiards/billiard_list.jinja",
            model={"billiard_clubs": billiard_clubs},
            context=context,
        )

    @get("/billiard-clubs/{billiard_club_id}")
    async def get_billiard_club_detail(
        self, billiard_club_id: UUID, billiard_club_detail_query: IBilliardClubDetailQuery
    ) -> Response:
        """Детальная информация по клубу"""

        billiard_club = await billiard_club_detail_query.query(billiard_club_id)

        return await self.view_async("billiards/billiard_card.jinja", model={"club": billiard_club})
