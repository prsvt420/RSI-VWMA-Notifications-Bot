import asyncio
import logging

from aiogram import Bot, Dispatcher, Router

from bot.handlers import setup_routers
from bot.middlewares import setup_middlewares
from config import BOT_TOKEN


async def main() -> None:
    bot: Bot = Bot(token=BOT_TOKEN)
    dispatcher: Dispatcher = Dispatcher()

    setup_middlewares(dispatcher)

    main_router: Router = setup_routers()

    dispatcher.include_router(router=main_router)

    dispatcher_task = asyncio.create_task(dispatcher.start_polling(bot))

    await asyncio.gather(dispatcher_task)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped!")
