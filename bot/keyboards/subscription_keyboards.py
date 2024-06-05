from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

subscription_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Продлить подписку\U0001F680', url='https://t.me/prsvt420')],
    [InlineKeyboardButton(text='Назад\U0001F519', callback_data='main_menu')],
])
