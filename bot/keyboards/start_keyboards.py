from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


start_menu_inline_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Начнем\U000026A1', callback_data='main_menu')],
])

main_menu_inline_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Подписка на уведомления\U0001F451', callback_data='subscription_menu')],
    [InlineKeyboardButton(text='Меню уведомлений\U0001F4DC', callback_data='notifications_menu')],
])
