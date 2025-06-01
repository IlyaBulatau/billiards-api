from enum import Enum


class TableType(Enum):
    SNOOKER = "Снукер"
    POOL = "Пул"
    RUSSIAN = "Русский"


class DayOfWeek(Enum):
    MONDAY = "Понедельник"
    TUESDAY = "Вторник"
    WEDNESDAY = "Среда"
    THURSDAY = "Четверг"
    FRIDAY = "Пятница"
    SATURDAY = "Суббота"
    SUNDAY = "Воскресенье"


class BookingStatus(Enum):
    PENDING = "Ожидание"
    CONFIRMED = "Подтверждено"
    CANCALLED = " Отменено"
    COMPLETED = "Завершено"
