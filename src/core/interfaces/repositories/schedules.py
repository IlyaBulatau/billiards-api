from core.interfaces.repositories.abstract import IRepository
from infrastructure.database.models.schedules import ClubSchedule


class IClubScheduleRepository(IRepository[ClubSchedule]):
    pass
