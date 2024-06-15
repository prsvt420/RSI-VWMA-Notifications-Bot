import math

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup

from bot.database.crud.notifications_crud import insert_notification, is_notification_exists, \
    insert_notification_user, is_notification_user_exists, select_notification, select_notifications_user_by_id, \
    select_notification_by_id, select_notification_by_user_id_and_notification_id, update_notification_user_status, \
    select_user_notifications_by_id
from bot.database.crud.users_crud import select_user_by_telegram_id, update_notifications_status
from bot.database.models import Users, Notifications, NotificationsUser
from bot.filters.subscription_filter import IsUserSubscribed
from bot.keyboards import notifications_keyboards
from bot.keyboards.notifications_keyboards import create_buttons_for_notifications_user, \
    add_more_inline_keyboard
from bot.utils.notifications_utils import get_interval_text, \
    is_valid_notification_data, interval_is_russian, convert_rus_interval_to_en

router = Router()


class Notification(StatesGroup):
    notification_data: State = State()


@router.callback_query(F.data == 'notifications_menu', IsUserSubscribed())
async def notifications_menu(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        text='Меню уведомлений\U0001F9FE', reply_markup=notifications_keyboards.notifications_menu_inline_keyboard
    )


@router.callback_query(F.data == 'notifications_settings', IsUserSubscribed())
async def notifications_settings(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        text='Настройки уведомлений\U0001F514',
        reply_markup=notifications_keyboards.notifications_settings_menu_inline_keyboard
    )


async def process_notifications_status_change(callback: CallbackQuery, status: bool) -> None:
    telegram_id: int = callback.from_user.id
    user: Users = await select_user_by_telegram_id(telegram_id)
    await update_notifications_status(user.id, status)
    status_text: str = 'выключены\U0001F515' if not status else 'включены\U0001F514'
    await callback.message.edit_text(
        text=f'Уведомления {status_text}',
        reply_markup=notifications_keyboards.back_to_notifications_settings_inline_keyboard
    )


@router.callback_query(F.data == 'notifications_on', IsUserSubscribed())
async def notifications_on(callback: CallbackQuery) -> None:
    await process_notifications_status_change(callback, True)


@router.callback_query(F.data == 'notifications_off', IsUserSubscribed())
async def notifications_off(callback: CallbackQuery) -> None:
    await process_notifications_status_change(callback, False)


@router.callback_query(F.data.startswith('notifications_list'), IsUserSubscribed())
async def notifications_list(callback: CallbackQuery, page: int = 1, per_page: int = 48) -> None:
    telegram_id: int = callback.from_user.id
    user: Users = await select_user_by_telegram_id(telegram_id)
    user_id: int = user.id

    notifications_user: list[NotificationsUser] = await select_notifications_user_by_id(user_id)

    if not notifications_user:
        await callback.message.edit_text(text='У вас нет уведомлений', reply_markup=notifications_keyboards.
                                         back_to_notifications_menu_inline_keyboard)
        return

    total_pages: int = math.ceil(len(notifications_user) / per_page)
    start_index: int = (page - 1) * per_page
    end_index: int = start_index + per_page
    paginated_notifications_user: list[NotificationsUser] = notifications_user[start_index:end_index]

    notifications_buttons: InlineKeyboardMarkup = await create_buttons_for_notifications_user(
        page,
        total_pages,
        start_index,
        paginated_notifications_user)

    text: str = ''

    for index, notification_user in enumerate(paginated_notifications_user):
        notification: Notifications = await select_notification_by_id(notification_user.notification_id)
        text_interval: str = await get_interval_text(notification.interval, 'ru')
        status: str = '\U00002705' if notification_user.is_active else '\U0000274C'
        text += (f'{start_index + index + 1}. '
                 f'{status} '
                 f'{notification.symbol} '
                 f'| {text_interval}\n')

    await callback.message.edit_text(text=text, reply_markup=notifications_buttons, parse_mode='html')


@router.callback_query(F.data.startswith('page_notifications_list_prev'), IsUserSubscribed())
async def notifications_list_prev(callback: CallbackQuery) -> None:
    page: int = int(callback.data.split('?page=')[-1]) - 1
    await notifications_list(callback, page)


@router.callback_query(F.data.startswith('page_notifications_list_next'), IsUserSubscribed())
async def notifications_list_next(callback: CallbackQuery) -> None:
    page: int = int(callback.data.split('?page=')[-1]) + 1
    await notifications_list(callback, page)


@router.callback_query(F.data.isdigit(), IsUserSubscribed())
async def button_notification_select(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        text=f'Настройка уведомления {int(callback.data) + 1}\U00002699',
        reply_markup=notifications_keyboards.notification_settings_inline_keyboard
    )


async def process_notification_status_change(callback: CallbackQuery, status: bool) -> None:
    message_text: str = callback.message.text
    index = int(message_text.split()[2].strip('⚙')) - 1
    telegram_id: int = callback.from_user.id
    user: Users = await select_user_by_telegram_id(telegram_id)
    user_id: int = user.id
    notifications: list[Notifications] = await select_user_notifications_by_id(user_id)
    selected_notification: Notifications = notifications[index]
    selected_user_notification: NotificationsUser = await select_notification_by_user_id_and_notification_id(
        user_id,
        selected_notification.id
    )
    await update_notification_user_status(selected_user_notification, status)
    status_text = 'выключено\U0001F515' if not status else 'включено\U0001F514'
    await callback.message.reply(text=f'Уведомление {status_text}')


@router.callback_query(F.data == 'notification_on', IsUserSubscribed())
async def notification_off(callback: CallbackQuery) -> None:
    await process_notification_status_change(callback, True)


@router.callback_query(F.data == 'notification_off', IsUserSubscribed())
async def notification_off(callback: CallbackQuery) -> None:
    await process_notification_status_change(callback, False)


@router.callback_query(F.data == 'add_new_notification', IsUserSubscribed())
async def add_new_notification(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Notification.notification_data)
    await callback.message.reply(text='Введите новое уведомление в формате [SYMBOL - INTERVAL]')


@router.message(Notification.notification_data)
async def notification_data(message: Message, state: FSMContext) -> None:

    validator_message: str = await is_valid_notification_data(message.text)

    if validator_message:
        await message.reply(text=validator_message)
        return

    symbol, interval = message.text.split('-')
    symbol, interval = symbol.strip().upper(), interval.strip()

    if await interval_is_russian(interval):
        interval: str = await convert_rus_interval_to_en(interval)

    await state.update_data(notification_data={'symbol': symbol, 'interval': interval})
    await state.clear()

    if not await is_notification_exists(symbol, interval):
        await insert_notification(symbol, interval)

    notification_id: int = (await select_notification(symbol, interval)).id
    user: Users = await select_user_by_telegram_id(message.from_user.id)

    if not await is_notification_user_exists(user.id, notification_id):
        await insert_notification_user(user.id, notification_id)
        await message.reply(
            text=f'Уведомление добавлено\U00002705',
            reply_markup=add_more_inline_keyboard
        )
    else:
        await message.reply(
            text=f'Такое уведомление уже добавлено\U0000274C',
            reply_markup=add_more_inline_keyboard
        )
