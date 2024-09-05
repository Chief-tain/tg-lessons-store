from typing import Any, Awaitable, Callable, get_type_hints

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot_app.application.payment_service import PaymentService


class PaymentServiceMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if PaymentService in data["_handler_dependencies"]:
            session = data["_session"]
            data["payment_service"] = PaymentService(session)
        return await handler(event, data)
