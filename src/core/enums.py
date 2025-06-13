from enum import Enum


class TableType(Enum):
    SNOOKER = "SNOOKER"
    POOL = "POOL"
    RUSSIAN = "RUSSIAN"


class DayOfWeek(Enum):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"


class BookingStatus(Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCALLED = " CANCALLED"
    COMPLETED = "COMPLETED"


def get_day_of_week_by_int(day: int) -> str:
    """Получить название дня недели в соответствии с номером недели, 0 - MONDAY, 6 - SUNDAY"""

    return DayOfWeek._member_names_[day]
