from datetime import datetime

from sqlalchemy import select

from bot.database.models import Subscriptions
from bot.database.engine import async_session_factory


async def is_user_subscribed(user_id: int) -> bool:
    async with async_session_factory() as async_session:
        return bool(
            await async_session.scalar(select(Subscriptions)
                                       .where(Subscriptions.user_id == user_id)
                                       .where(Subscriptions.subscription_end_datetime > datetime.now())))


async def select_subscription_by_user_id(user_id: int) -> Subscriptions:
    async with async_session_factory() as async_session:
        return await async_session.scalar(select(Subscriptions).where(Subscriptions.user_id == user_id))


async def insert_subscription(user_id: int, subscription_end_datetime: datetime) -> None:
    async with async_session_factory() as async_session:
        subscription: Subscriptions = Subscriptions(
            user_id=user_id,
            subscription_end_datetime=subscription_end_datetime
        )
        async_session.add(subscription)
        await async_session.commit()


async def update_subscription(user_id: int, subscription_end_datetime: datetime) -> None:
    async with async_session_factory() as async_session:
        subscription = await async_session.scalar(select(Subscriptions).where(Subscriptions.user_id == user_id))
        subscription.subscription_end_datetime = subscription_end_datetime
        await async_session.commit()
