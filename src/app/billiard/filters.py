from core.filters.filter_model import FilterModel
from infrastructure.database.models import BilliardClub


class BilliardClubFilter(FilterModel[BilliardClub]):
    name: str | None = None
    name__ilike: str | None = None

    class Model:
        target = BilliardClub
