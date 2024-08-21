import asyncio
import logging
import json

from aiogram import Bot, Dispatcher
from aiogram.utils.i18n import I18n
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats

from bot_app.tg import routers
from bot_app.modules.redis_storage_custom_keys import RedisStorageCustomKeys

from shared import settings

logging.getLogger().setLevel(logging.INFO)


def my_json_loads(data: str):
    data_dict = json.loads(data)
    return_data = {}
    for key, value in data_dict.items():
        if key != "channels":
            return_data[key] = value
        else:
            return_data[key] = [ch_val for ch_val in value]
    return return_data


def my_json_dumps(data: dict):
    jsonable_data = {}
    for key, value in data.items():
        if key != "channels":
            jsonable_data[key] = value
        else:
            jsonable_data[key] = [ch_val.__dict__ for ch_val in value]
    return json.dumps(jsonable_data)


async def main():

    logging.info("Starting...")

    storage = RedisStorageCustomKeys.from_url(
        f"redis://{settings.REDIS_HOST}/{settings.REDIS_DB}",
        json_loads=my_json_loads,
        json_dumps=my_json_dumps,
    )

    dp = Dispatcher(storage=storage)

    for router in routers:
        dp.include_router(router)

    bot = Bot(token=settings.TELEGRAM_TOKEN, parse_mode=ParseMode.MARKDOWN_V2)

    await bot.set_my_commands(
        commands=[
            BotCommand(command="start", description="Начало работы"),
            BotCommand(command="help", description="Описание режимов работы"),
        ],
        scope=BotCommandScopeAllPrivateChats(),
        language_code=None,
    )

    logging.info("Starting polling...")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
