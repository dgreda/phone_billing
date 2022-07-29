import calendar
from datetime import datetime, timezone


class DateService:
    @staticmethod
    def get_month_start_utc_timestamp(year: int, month: int) -> datetime:
        return datetime(
            year, month, 1, hour=0, minute=0, second=0, tzinfo=timezone.utc
        )

    @staticmethod
    def get_month_end_utc_timestamp(year: int, month: int) -> datetime:
        last_day_of_month = calendar.monthrange(year, month)[1]
        return datetime(
            year,
            month,
            last_day_of_month,
            hour=23,
            minute=59,
            second=59,
            tzinfo=timezone.utc,
        )
