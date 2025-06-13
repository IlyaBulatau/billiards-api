from core.filters.filter_model import FilterModel
from infrastructure.database.models import BookingTable


class BookingFilter(FilterModel[BookingTable]):
    class Model:
        target = BookingTable
