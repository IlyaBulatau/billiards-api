from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from core.filters.filter_model import FilterModel
from core.filters.sqlalchemy import orm_filter
from core.interfaces.repositories import IBilliardClubRepository, IBilliardTableRepository
from core.schemes.paginations import Pagination
from infrastructure.database.models import BilliardClub, BilliardTable


class BilliarClubRepository(IBilliardClubRepository):
    async def get_all(
        self, filters: FilterModel[BilliardClub], pagination: Pagination
    ) -> list[BilliardClub]:
        stmt = orm_filter(
            filters,
            select(BilliardClub)
            .limit(pagination.limit)
            .offset(pagination.offset)
            .options(joinedload(BilliardClub.address), selectinload(BilliardClub.schedules)),
        )
        result = await self._async_session.execute(stmt)

        return result.scalars().all()

    async def get_by_id(self, billiard_club_id: UUID) -> BilliardClub | None:
        stmt = (
            select(BilliardClub)
            .where(BilliardClub.id == billiard_club_id)
            .options(
                joinedload(BilliardClub.address),
                selectinload(BilliardClub.schedules),
                selectinload(BilliardClub.billiard_tables).selectinload(BilliardTable.bookings),
            )
        )

        result = await self._async_session.execute(stmt)

        return result.scalar_one_or_none()

    async def create(self, instance: BilliardClub) -> BilliardClub: ...

    async def update(self, instance: BilliardClub) -> BilliardClub: ...

    async def delete(self, instance: BilliardClub) -> None: ...


class BilliarTableRepository(IBilliardTableRepository):
    async def get_all(self): ...

    async def create(self): ...

    async def update(self): ...

    async def delete(self): ...

    async def get_by_id_with_club_and_schedules(
        self, billiard_table_id: UUID
    ) -> BilliardTable | None:
        stmt = (
            select(BilliardTable)
            .where(BilliardTable.id == billiard_table_id)
            .options(joinedload(BilliardTable.billibard_club).selectinload(BilliardClub.schedules))
        )

        result = await self._async_session.execute(stmt)

        return result.scalar_one_or_none()
