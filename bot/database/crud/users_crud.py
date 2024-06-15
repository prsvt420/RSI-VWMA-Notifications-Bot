from datetime import datetime

from sqlalchemy import select, Result

from bot.database.engine import async_session_factory
from bot.database.models import Users, NotificationsUser, Subscriptions


async def is_user_registered(telegram_id: int) -> bool:
    async with async_session_factory() as async_session:
        return bool(await async_session.scalar(select(Users).where(Users.telegram_id == telegram_id)))


async def user_is_supeurser(telegram_id: int) -> bool:
    async with async_session_factory() as async_session:
        return bool(await async_session.scalar(
            select(Users).where(Users.telegram_id == telegram_id).where(Users.is_superuser == 1)
        ))


async def select_user_by_telegram_id(telegram_id: int) -> Users:
    async with async_session_factory() as async_session:
        return await async_session.scalar(select(Users).where(Users.telegram_id == telegram_id))


async def select_all_users() -> list[Users]:
    async with async_session_factory() as async_session:
        return list(await async_session.scalars(select(Users)))


async def select_users_by_notification_id(notification_id) -> list[Users]:
    async with async_session_factory() as async_session:
        users: Result[tuple[Users]] = await async_session.execute(
            select(Users).join(NotificationsUser).join(Subscriptions)
            .where(NotificationsUser.notification_id == notification_id)
            .where(NotificationsUser.is_active == 1)
            .where(Users.is_notifications_enabled == 1)
            .where(Subscriptions.subscription_end_datetime > datetime.now())
        )
    return list(users.scalars().all())


async def insert_user(telegram_id: int) -> None:
    async with async_session_factory() as async_session:
        user: Users = Users(telegram_id=telegram_id, is_notifications_enabled=1, is_superuser=0)
        async_session.add(user)
        await async_session.commit()


async def update_notifications_status(user_id: int, status: bool) -> None:
    async with async_session_factory() as async_session:
        user: Users = await async_session.scalar(select(Users).where(Users.id == user_id))
        user.is_notifications_enabled = status
        await async_session.commit()
