import asyncio
import logging
import json

from aiogram import Bot, Dispatcher
from aiogram.utils.i18n import I18n
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats

from bot_app.modules.di import hang_out_the_flags
from bot_app.tg import routers
from bot_app.modules.redis_storage_custom_keys import RedisStorageCustomKeys
from bot_app.tg.middlewares import (
    UserServiceMiddleware,
    PostgresqlSessionMiddleware,
    LessonServiceMiddleware,
    PaymentServiceMiddleware,
    MinioMediaServiceMiddleware,
)

from shared import settings
from shared.dbs.postgresql import async_session_noauto as pool

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

    session_di_middleware = PostgresqlSessionMiddleware(pool=pool)
    dp.message.middleware(session_di_middleware)
    dp.callback_query.middleware(session_di_middleware)
    dp.inline_query.middleware(session_di_middleware)
    dp.my_chat_member.middleware(session_di_middleware)

    # user service middleware setup
    user_middleware = UserServiceMiddleware()
    dp.message.middleware(user_middleware)
    dp.callback_query.middleware(user_middleware)
    dp.my_chat_member.middleware(user_middleware)
    logging.info("User middleware set up")

    # lesson service middleware setup
    lesson_middleware = LessonServiceMiddleware()
    dp.message.middleware(lesson_middleware)
    dp.callback_query.middleware(lesson_middleware)
    dp.my_chat_member.middleware(lesson_middleware)
    logging.info("Lesson middleware set up")

    # payment service middleware setup
    payment_middleware = PaymentServiceMiddleware()
    dp.message.middleware(payment_middleware)
    dp.callback_query.middleware(payment_middleware)
    dp.my_chat_member.middleware(payment_middleware)
    logging.info("Payment middleware set up")

    # minio media middleware set up
    minio_media_middleware = MinioMediaServiceMiddleware()
    dp.message.middleware(minio_media_middleware)
    dp.callback_query.middleware(minio_media_middleware)
    logging.info("Minio Media Service Middleware set up")

    for router in routers:
        dp.include_router(router)

    # add "is_using_postgres" flags to all corresponding handlers
    hang_out_the_flags(dp)

    bot = Bot(token=settings.TELEGRAM_TOKEN, parse_mode="HTML")

    await bot.set_my_commands(
        commands=[
            BotCommand(command="start", description="Начало работы"),
            BotCommand(command="help", description="Описание режимов работы"),
            BotCommand(
                command="english_lessons", description="Уроки английского языка"
            ),
            BotCommand(command="chinese_lessons", description="Уроки китайского языка"),
        ],
        scope=BotCommandScopeAllPrivateChats(),
        language_code=None,
    )

    logging.info("Starting polling...")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
