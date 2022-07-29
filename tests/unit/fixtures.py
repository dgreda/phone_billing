from datetime import datetime, timedelta
from random import randint

from app.domain.entities import Call


def create_call(duration: int, user_id: int = 1) -> Call:
    recipient_country_code = randint(1, 100)
    recipient_number = randint(101_100_100, 959_000_1000)
    now = datetime.now()
    start_datetime = now - timedelta(minutes=duration)
    end_datetime = now

    return Call(
        recipient_country_code=recipient_country_code,
        recipient_number=recipient_number,
        duration_in_minutes=duration,
        start_datetime_iso_8601=start_datetime,
        end_datetime_iso_8601=end_datetime,
        user_id=user_id,
    )
