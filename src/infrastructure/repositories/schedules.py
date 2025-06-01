from sqlalchemy.dialects.postgresql import insert

from core.filters.filter_model import FilterModel
from core.interfaces.repositories.schedules import IClubScheduleRepository
from core.schemes.paginations import Pagination
from infrastructure.database.models.schedules import ClubSchedule


class ClubScheduleRepository(IClubScheduleRepository):
    async def get_all(
        self, filters: FilterModel[ClubSchedule], pagination: Pagination
    ) -> list[ClubSchedule]: ...

    async def create(self, instance: ClubSchedule) -> ClubSchedule:
        stmt = (
            insert(ClubSchedule)
            .values(
                billiard_club_id=instance.billiard_club_id,
                day_of_week=instance.day_of_week,
                opening_time=instance.opening_time,
                closing_time=instance.closing_time,
            )
            .on_conflict_do_nothing()
        ).returning(ClubSchedule)

        result = await self._async_session.execute(stmt)

        return result.scalar_one_or_none()

    async def update(self, instance: ClubSchedule) -> ClubSchedule: ...

    async def delete(self, instance: ClubSchedule) -> None: ...
