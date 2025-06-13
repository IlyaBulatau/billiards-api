from core.filters.filter_model import FilterModel
from infrastructure.database.models import ClubSchedule


class ScheduleFilter(FilterModel[ClubSchedule]):
    class Model:
        target = ClubSchedule
