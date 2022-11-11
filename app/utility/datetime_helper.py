from datetime import date, datetime, timezone, timedelta
from typing import Optional


class DateTimeHelper:

    @staticmethod
    def get_today_with_timezone(shift_day: Optional[int] = None):
        today = datetime.combine(date.today(), datetime.min.time())

        if shift_day is not None:
            today = today + timedelta(days=shift_day)

        date_with_timezone = today.astimezone(
            timezone(timedelta(hours=8)))  # Taipei,Taiwan timezone

        return date_with_timezone
