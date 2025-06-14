from datetime import date, datetime, time, timedelta


def get_previous_day(target_dt: datetime) -> datetime:
    return target_dt - timedelta(days=1)


def build_dt(date: date, time: time) -> datetime:
    """Получить обьект datetime из даты и времени"""

    return datetime.combine(date, time)
