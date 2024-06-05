from aiogram import Dispatcher

from bot.middlewares.registration_middleware import RegistrationMiddleware


def setup_middlewares(dispatcher: Dispatcher) -> None:
    dispatcher.message.outer_middleware(RegistrationMiddleware())
