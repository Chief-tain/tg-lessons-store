from bot_app.tg.handlers.help import help_router
from bot_app.tg.handlers.start import start_router
from bot_app.tg.handlers.lessons import lessons_router


routers = [start_router, help_router, lessons_router]


__all__ = ("start_router", "help_router", "lessons_router")
