from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot_app.application.minio_service import OrderMediaRepository
from shared.dbs.minio_async import client


class MinioMediaServiceMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if OrderMediaRepository in data["_handler_dependencies"]:
            data["order_media_minio"] = OrderMediaRepository(client)
        return await handler(event, data)
