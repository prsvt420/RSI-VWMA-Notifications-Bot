from aiogram import Router
from aiogram.filters import CommandStart

from bot.keyboards import start_keyboard

router: Router = Router()


@router.message(CommandStart())
async def cmd_start(message) -> None:
    await message.reply(f'Приветствую тебя! Начнем?', reply_markup=start_keyboard.inline_keyboard)
