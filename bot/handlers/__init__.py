from aiogram import Router
from . import start_handlers, subscription_handlers, notifications_handlers, admin_handlers


def setup_routers() -> Router:
    main_router: Router = Router()

    main_router.include_routers(
        start_handlers.router,
        subscription_handlers.router,
        notifications_handlers.router,
        admin_handlers.router
    )
    return main_router
