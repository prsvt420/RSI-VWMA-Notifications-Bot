from datetime import datetime


async def is_valid_datetime(datetime_: str) -> bool:
    try:
        datetime.strptime(datetime_, '%d.%m.%Y %H:%M')
        return True
    except ValueError:
        return False
