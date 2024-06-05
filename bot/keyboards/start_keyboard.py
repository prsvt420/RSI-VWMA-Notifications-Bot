from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


inline_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Начнем\U000026A1', callback_data='start_menu')],
])
