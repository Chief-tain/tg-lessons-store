from bot_app.tg.handlers.help import help_router
from bot_app.tg.handlers.start import start_router
from bot_app.tg.handlers.lessons import lessons_router
from bot_app.tg.handlers.yookassa import yookass_router
from bot_app.tg.handlers.personal_account import personal_account_router
from bot_app.tg.handlers.moderator import moderator_router


routers = [
    start_router,
    help_router,
    lessons_router,
    yookass_router,
    personal_account_router,
    moderator_router,
]


__all__ = (
    "start_router",
    "help_router",
    "lessons_router",
    "yookass_router",
    "personal_account_router",
    "moderator_router",
)
