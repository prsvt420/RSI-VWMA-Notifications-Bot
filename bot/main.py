import asyncio
import logging

from aiogram import Bot, Dispatcher

from bot.handlers import start_handler
from bot.middlewares import setup_middlewares
from config import BOT_TOKEN


async def main() -> None:
    bot: Bot = Bot(token=BOT_TOKEN)
    dispatcher: Dispatcher = Dispatcher()

    setup_middlewares(dispatcher)

    dispatcher.include_routers(
        start_handler.router
    )

    dispatcher_task = asyncio.create_task(dispatcher.start_polling(bot))

    await asyncio.gather(dispatcher_task)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped!")
