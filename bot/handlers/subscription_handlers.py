from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.database.crud.subscription_crud import is_user_subscribed, select_subscription_by_user_id
from bot.database.crud.users_crud import select_user_by_telegram_id
from bot.database.models import Users, Subscriptions
from bot.keyboards import subscription_keyboards

router: Router = Router()


@router.callback_query(F.data == 'subscription_menu')
async def subscribe_menu(callback: CallbackQuery) -> None:
    user: Users = await select_user_by_telegram_id(callback.from_user.id)

    if await is_user_subscribed(user.id):
        subscribed: Subscriptions = await select_subscription_by_user_id(user.id)
        subscription_end_datetime = subscribed.subscription_end_datetime.strftime('%d-%m-%Y %H:%M:%S')
        message: str = f'Подписка активна\U0001F48E\nОкончание подписки: {subscription_end_datetime}\U0000231B'
    else:
        message: str = 'Подписка не активна\U0000274C'

    await callback.message.edit_text(message, reply_markup=subscription_keyboards.subscription_menu_keyboard)
