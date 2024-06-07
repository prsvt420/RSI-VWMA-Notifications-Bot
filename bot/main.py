import asyncio
import logging

from aiogram import Bot, Dispatcher, Router

from bot.handlers import setup_routers
from bot.middlewares import setup_middlewares
from bot.services.notifications_service.notifications_logic import handle_notifications, \
    handle_storage_sent_notifications
from bot.config import BOT_TOKEN


async def main() -> None:
    bot: Bot = Bot(token=BOT_TOKEN)
    dispatcher: Dispatcher = Dispatcher()

    setup_middlewares(dispatcher)

    main_router: Router = setup_routers()

    dispatcher.include_router(router=main_router)

    notifications_task = asyncio.create_task(handle_notifications(bot))
    dispatcher_task = asyncio.create_task(dispatcher.start_polling(bot))
    storage_sent_notifications_task = asyncio.create_task(handle_storage_sent_notifications())

    await asyncio.gather(dispatcher_task, storage_sent_notifications_task, notifications_task)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped!")
