from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admin_menu_inline_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Продлить подписку пользователю\U0001F511', callback_data='extend_subscription')],
        [InlineKeyboardButton(text='Получить список пользователей\U0001F4CB', callback_data='get_list_users___')],
        [InlineKeyboardButton(text='Назад\U0001F519', callback_data='main_menu')],
    ]
)

back_to_admin_menu_inline_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Назад\U0001F519', callback_data='admin_menu')],
    ]
)
