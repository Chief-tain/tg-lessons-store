from bot_app.tg.handlers.help import help_router
from bot_app.tg.handlers.start import start_router
from bot_app.tg.handlers.lessons import lessons_router
from bot_app.tg.handlers.yookassa import yookass_router


routers = [start_router, help_router, lessons_router, yookass_router]


__all__ = ("start_router", "help_router", "lessons_router", "yookass_router")
