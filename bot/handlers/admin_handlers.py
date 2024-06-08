import logging
from datetime import datetime

import aiofiles
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, FSInputFile

from bot.database.crud.subscription_crud import update_subscription, select_subscription_by_user_id
from bot.database.crud.users_crud import is_user_registered, select_user_by_telegram_id, select_all_users
from bot.database.models import Users, Subscriptions
from bot.keyboards import admin_keyboards
from bot.utils.admin_utils import is_valid_datetime

router: Router = Router()


class Subscription(StatesGroup):
    telegram_id: State = State()
    new_datetime: State = State()


@router.callback_query(F.data == 'admin_menu')
async def admin_menu(callback: CallbackQuery) -> None:
    await callback.message.edit_text(f'Админ меню\U0001F4DC', reply_markup=admin_keyboards.admin_menu_inline_keyboard)


@router.callback_query(F.data == 'extend_subscription')
async def extend_subscription(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Subscription.telegram_id)
    await callback.message.reply(f'Введите telegram id пользователя')


@router.message(Subscription.telegram_id)
async def extend_subscription(message: Message, state: FSMContext) -> None:
    telegram_id: str = message.text

    if not telegram_id.isdigit():
        await message.reply(f'Введен некорректный telegram id, попробуйте ещё раз')
        return

    telegram_id: int = int(telegram_id)

    if not await is_user_registered(telegram_id):
        await message.reply(f'Пользователь {telegram_id} не зарегистрирован, попробуйте ещё раз')
        return

    await state.update_data(telegram_id=message.text)
    await message.reply(f'Введите дату окончания подписки')
    await state.set_state(Subscription.new_datetime)


@router.message(Subscription.new_datetime)
async def extend_subscription(message: Message, state: FSMContext) -> None:
    new_datetime: str = message.text

    await state.update_data(new_datetime=new_datetime)

    if not await is_valid_datetime(new_datetime):
        await message.reply('Некорректная дата окончания подписки. Введите дату в формате DD.MM.YYYY HH:MM')
        return

    new_datetime: datetime = datetime.strptime(new_datetime, '%d.%m.%Y %H:%M')

    subscription_data = await state.get_data()

    telegram_id: int = subscription_data.get('telegram_id')
    user_id: int = (await select_user_by_telegram_id(telegram_id)).id

    await update_subscription(user_id, new_datetime)

    await message.reply(
        f'Подписка пользователя с telegram id {telegram_id} будет продлена до {new_datetime}',
        reply_markup=admin_keyboards.back_to_admin_menu_inline_keyboard
    )

    logging.info(f'{telegram_id} extended subscription to {new_datetime}')

    await state.clear()


@router.callback_query(F.data == 'get_list_users___')
async def get_list_users(callback: CallbackQuery) -> None:
    users: list[Users] = await select_all_users()

    async with aiofiles.open('logs/users.log', 'w') as f:
        await f.write('telegram id'.ljust(21) + 'subscription end datetime\n\n')
        for user in users:
            subscription: Subscriptions = await select_subscription_by_user_id(user.id)

            telegram_id: str = str(user.telegram_id).ljust(20)
            subscription_end_datetime: str = str(subscription.subscription_end_datetime).ljust(30)
            await f.write(f'{telegram_id} {subscription_end_datetime}\n')

    await callback.message.reply_document(
        FSInputFile('logs/users.log', filename='users.log'),
    )
