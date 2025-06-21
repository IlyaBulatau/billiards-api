from core.filters.filter_model import FilterModel
from infrastructure.database.models import BilliardClub


class BilliardClubFilter(FilterModel[BilliardClub]):
    name: str | None = None
    name__ilike: str | None = None
    has_snooker: bool | None = None
    has_pool: bool | None = None
    has_russian: bool | None = None
    min_price_for_table__lte: float | None = None
    min_price_for_table__gte: float | None = None
    is_work_now: bool | None = None

    class Model:
        target = BilliardClub
