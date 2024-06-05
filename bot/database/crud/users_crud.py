from sqlalchemy import select

from bot.database.models import Users
from bot.database.engine import async_session_factory


async def is_user_registered(telegram_id: int) -> bool:
    async with async_session_factory() as async_session:
        return bool(await async_session.scalar(select(Users).where(Users.telegram_id == telegram_id)))


async def insert_user(telegram_id: int) -> None:
    async with async_session_factory() as async_session:
        user: Users = Users(telegram_id=telegram_id, is_subscribed=0, is_superuser=0)
        async_session.add(user)
        await async_session.commit()
