from sqlalchemy import select, Result

from bot.database.engine import async_session_factory
from bot.database.models import Notifications, NotificationsUser


async def is_notification_exists(symbol: str, interval: str) -> bool:
    async with async_session_factory() as async_session:
        return bool(
            await async_session.scalar(
                select(Notifications)
                .where(Notifications.symbol == symbol)
                .where(Notifications.interval == interval))
        )


async def is_notification_user_exists(user_id: int, notification_id: int) -> bool:
    async with async_session_factory() as async_session:
        return bool(
            await async_session.scalar(
                select(NotificationsUser)
                .where(NotificationsUser.user_id == user_id)
                .where(NotificationsUser.notification_id == notification_id))
        )


async def select_notification(symbol: str, interval: str) -> Notifications:
    async with async_session_factory() as async_session:
        return await async_session.scalar(
            select(Notifications)
            .where(Notifications.symbol == symbol)
            .where(Notifications.interval == interval)
        )


async def select_notifications() -> list[Notifications]:
    async with async_session_factory() as async_session:
        notifications: Result[tuple[Notifications]] = await async_session.execute(select(Notifications))
    return list(notifications.scalars().all())


async def select_notifications_user_by_id(user_id: int) -> list[NotificationsUser]:
    async with async_session_factory() as async_session:
        notifications: Result[tuple[NotificationsUser]] = await async_session.execute(
            select(NotificationsUser)
            .where(NotificationsUser.user_id == user_id)
        )
    return list(notifications.scalars().all())


async def select_notification_by_user_id_and_notification_id(user_id: int, notification_id: int) -> NotificationsUser:
    async with async_session_factory() as async_session:
        return await async_session.scalar(
            select(NotificationsUser)
            .where(NotificationsUser.user_id == user_id)
            .where(NotificationsUser.notification_id == notification_id)
        )


async def select_notification_by_id(notification_id: int) -> Notifications:
    async with async_session_factory() as async_session:
        return await async_session.scalar(
            select(Notifications)
            .where(Notifications.id == notification_id)
        )


async def select_user_notifications_by_id(user_id: int) -> list[Notifications]:
    async with async_session_factory() as async_session:
        notifications = await async_session.execute(
            select(Notifications).join(NotificationsUser)
            .where(NotificationsUser.user_id == user_id)
        )
        return list(notifications.scalars().all())


async def insert_notification(
        symbol: str,
        interval: str,
        rsi_period: int = 6,
        ma_period: int = 4) -> None:
    async with async_session_factory() as async_session:
        notification: Notifications = Notifications(
            symbol=symbol,
            interval=interval,
            rsi_period=rsi_period,
            ma_period=ma_period
        )
        async_session.add(notification)
        await async_session.commit()


async def insert_notification_user(user_id: int, notification_id: int) -> None:
    async with async_session_factory() as async_session:
        notification_user: NotificationsUser = NotificationsUser(
            user_id=user_id,
            notification_id=notification_id,
            is_active=True
        )
        async_session.add(notification_user)
        await async_session.commit()


async def update_notification_user_status(notification_user: NotificationsUser, status: bool) -> None:
    async with async_session_factory() as async_session:
        notification_user.is_active = status
        async_session.add(notification_user)
        await async_session.commit()
