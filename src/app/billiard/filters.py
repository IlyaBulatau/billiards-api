from core.filters.filter_model import FilterModel
from infrastructure.database.models import BilliardClub


class BilliardClubFilter(FilterModel[BilliardClub]):
    name: str | None = None
    name__ilike: str | None = None
    has_snooker: bool | None = None
    has_pool: bool | None = None
    has_russian: bool | None = None

    class Model:
        target = BilliardClub
