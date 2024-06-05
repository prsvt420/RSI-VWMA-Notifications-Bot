from aiogram import Dispatcher

from bot.middlewares.registration_middleware import RegistrationMiddleware
from bot.middlewares.subscription_middleware import SubscriptionMiddleware


def setup_middlewares(dispatcher: Dispatcher) -> None:
    dispatcher.message.outer_middleware(RegistrationMiddleware())
    dispatcher.message.outer_middleware(SubscriptionMiddleware())
