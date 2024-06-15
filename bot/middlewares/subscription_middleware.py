from datetime import datetime, timedelta
from typing import Callable, Any, Awaitable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot.database.crud.subscription_crud import insert_subscription, select_subscription_by_user_id
from bot.database.crud.users_crud import select_user_by_telegram_id
from bot.database.models import Users


class SubscriptionMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:

        telegram_id: int = event.from_user.id
        user: Users = await select_user_by_telegram_id(telegram_id)

        if not await select_subscription_by_user_id(user_id=user.id):
            current_datetime: datetime = datetime.now()
            subscription_end_datetime: datetime = current_datetime + timedelta(hours=24)

            await insert_subscription(user_id=user.id, subscription_end_datetime=subscription_end_datetime)

        return await handler(event, data)
