from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from bot.keyboards import start_keyboards

router: Router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.reply(f'Приветствую тебя! Начнем?', reply_markup=start_keyboards.start_menu_inline_keyboard)


@router.callback_query(F.data == 'main_menu')
async def start_menu(callback: CallbackQuery) -> None:
    await callback.message.edit_text(f'Меню\U0001F4DC', reply_markup=start_keyboards.main_menu_inline_keyboard)
