from typing import get_type_hints

from aiogram import Dispatcher
from sqlalchemy.ext.asyncio import AsyncSession


def hang_out_the_flags(dispatcher: Dispatcher):
    for router in dispatcher.sub_routers:
        for update_name, observer in router.observers.items():
            if len(observer.handlers) == 0:
                continue
            for handler in observer.handlers:
                handler_dependencies = []
                hints = get_type_hints(handler.callback)
                for name, type_ in hints.items():
                    if type_.__module__.startswith("aiogram."):
                        continue
                    if type_.__module__.startswith("bot_app.tg.callbacks."):
                        continue
                    if type_.__module__.startswith("shared.telegram.callbacks."):
                        continue
                    if type_.__module__.startswith("structlog."):
                        continue
                    handler_dependencies.append(type_)
                for dep in handler_dependencies:
                    hints = get_type_hints(dep.__init__)
                    hints.pop("return", None)
                    if AsyncSession in hints.values():
                        handler.flags["is_using_postgres"] = True
                        break
