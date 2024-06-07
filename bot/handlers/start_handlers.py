from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from bot.database.crud.users_crud import user_is_supeurser
from bot.keyboards import start_keyboards

router: Router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.reply(f'Приветствую тебя! Начнем?', reply_markup=start_keyboards.start_menu_inline_keyboard)


@router.callback_query(F.data == 'main_menu')
async def main_menu(callback: CallbackQuery) -> None:
    telegram_id: int = callback.from_user.id
    keyboard: InlineKeyboardMarkup = start_keyboards.main_menu_inline_keyboard
    admin_button: list[InlineKeyboardButton] = start_keyboards.admin_menu_inline_keyboard_button

    if await user_is_supeurser(telegram_id) and admin_button not in keyboard.inline_keyboard:
        keyboard.inline_keyboard.append(admin_button)

    await callback.message.edit_text(f'Меню\U0001F4DC', reply_markup=keyboard)
