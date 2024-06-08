from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery

from bot.database.crud.subscription_crud import is_user_subscribed
from bot.database.crud.users_crud import select_user_by_telegram_id
from bot.database.models import Users
from bot.keyboards import subscription_keyboards


class IsUserSubscribed(BaseFilter):

    async def __call__(self, callback: CallbackQuery) -> bool:
        telegram_id: int = callback.from_user.id
        user: Users = await select_user_by_telegram_id(telegram_id)
        is_subscribed: bool = await is_user_subscribed(user_id=user.id)

        if is_subscribed:
            return True

        await callback.message.edit_text(
            'У вас нет подписки на уведомления!',
            reply_markup=subscription_keyboards.subscription_menu_inline_keyboard)

        return False
