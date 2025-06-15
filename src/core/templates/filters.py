from datetime import datetime, time

from core.enums import get_day_of_week_by_int
from core.templates.decorators import template_filter


__all__ = ("TimeFormatFilter",)


days = {
    "monday": "Понедельник",
    "tuesday": "Вторник",
    "wednesday": "Среда",
    "thursday": "Четверг",
    "friday": "Пятница",
    "saturday": "Суббота",
    "sunday": "Воскресенье",
}


@template_filter("format_time")
class TimeFormatFilter:
    def __call__(self, time: time) -> str:
        return time.strftime("%H:%M")


@template_filter("day_of_week_format")
class DayOfWeekFormatFilter:
    def __call__(self, day_of_week: str) -> str:
        return days.get(day_of_week.lower(), day_of_week)


@template_filter("format_dt")
class DatetimeFormatFilter:
    def __call__(self, dt: datetime) -> str:
        day_of_week = dt.weekday()

        rus_weekday = days[get_day_of_week_by_int(day_of_week).lower()]

        return f"{rus_weekday} {dt.strftime('%H:%M')}"
