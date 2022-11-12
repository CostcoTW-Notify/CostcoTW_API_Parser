from datetime import date, datetime, timezone, timedelta, tzinfo
from typing import Optional


class DateTimeHelper:

    @staticmethod
    def get_today_with_timezone(shift_day: Optional[int] = None):
        today = date.today()
        today_with_tz = datetime(today.year, today.month, today.day, 0,
                                 0, 0, 0, tzinfo=timezone(timedelta(hours=8)))

        if shift_day is not None:
            today_with_tz = today_with_tz + timedelta(days=shift_day)

        return today_with_tz
