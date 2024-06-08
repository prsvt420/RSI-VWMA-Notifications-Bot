import logging
from typing import Callable, Any, Awaitable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot.database.crud.users_crud import is_user_registered, insert_user


class RegistrationMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:

        telegram_id: int = event.from_user.id

        if not await is_user_registered(telegram_id):
            await insert_user(telegram_id)

            logging.info(f'{telegram_id} registered')

        return await handler(event, data)
