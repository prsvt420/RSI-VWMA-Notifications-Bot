from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.database.models import NotificationsUser

notifications_menu_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Настройки уведомлений\U0001F514', callback_data='notifications_settings')],
    [InlineKeyboardButton(
        text='Список ваших уведомлений\U0001F4DD', callback_data='notifications_list'
    )],
    [InlineKeyboardButton(text='Добавить новое уведомление\U0001F514', callback_data='add_new_notification')],
    [InlineKeyboardButton(text='Назад\U0001F519', callback_data='main_menu')],
])

notifications_settings_menu_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Включить уведомления\U0001F514', callback_data='notifications_on')],
    [InlineKeyboardButton(text='Выключить уведомления\U0001F515', callback_data='notifications_off')],
    [InlineKeyboardButton(text='Назад\U0001F519', callback_data='notifications_menu')],
])

back_to_notifications_settings_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад\U0001F519', callback_data='notifications_settings')],
])

back_to_notifications_menu_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад\U0001F519', callback_data='notifications_menu')],
])

add_more_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить еще', callback_data='add_new_notification')],
    [InlineKeyboardButton(text='Назад\U0001F519', callback_data='notifications_menu')],
])

notification_settings_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Включить уведомление\U0001F514', callback_data='notification_on')],
    [InlineKeyboardButton(text='Выключить уведомление\U0001F515', callback_data='notification_off')],
    [InlineKeyboardButton(text='Назад\U0001F519', callback_data='notifications_list')],
])


async def create_buttons_for_notifications_user(
        page: int,
        total_pages: int,
        start_index: int,
        notifications_user: list[NotificationsUser]) -> InlineKeyboardMarkup:
    inline_keyboard: list[list[InlineKeyboardButton]] = []
    row: list[InlineKeyboardButton] = []

    for index, notification in enumerate(notifications_user):
        actual_index: int = start_index + index
        inline_keyboard_button: InlineKeyboardButton = InlineKeyboardButton(
            text=str(actual_index + 1), callback_data=str(actual_index)
        )
        row.append(inline_keyboard_button)
        if len(row) == 4:
            inline_keyboard.append(row)
            row: list[InlineKeyboardButton] = []

    if row:
        while len(row) < 4:
            row.append(InlineKeyboardButton(text=' ', callback_data=' '))
        inline_keyboard.append(row)

    await create_pagination_buttons(inline_keyboard, page, total_pages)
    inline_keyboard.append([InlineKeyboardButton(text='Назад\U0001F519', callback_data='notifications_menu')])
    reply_keyboard_markup: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return reply_keyboard_markup


async def create_pagination_buttons(inline_keyboard, page, total_pages) -> None:
    if total_pages == 1:
        inline_keyboard.append([
            InlineKeyboardButton(text=' ', callback_data=' '),
            InlineKeyboardButton(
                text=f'{page}/{total_pages}',
                callback_data=f'notifications_list?page={page}'
            ),
            InlineKeyboardButton(text=' ', callback_data=' ')
        ])
    else:
        buttons: list[InlineKeyboardButton] = [
            InlineKeyboardButton(text='←', callback_data=f'page_notifications_list_prev?page={page}'),
            InlineKeyboardButton(
                text=f'{page}/{total_pages}',
                callback_data=f'user_notifications_list?page={page}'
            ),
            InlineKeyboardButton(text='→', callback_data=f'page_notifications_list_next?page={page}')
        ]
        if page == 1:
            buttons[0] = InlineKeyboardButton(text=' ', callback_data=' ')
        elif page == total_pages:
            buttons[2] = InlineKeyboardButton(text=' ', callback_data=' ')
        inline_keyboard.append(buttons)
