from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats


async def set_bot_commands(bot: Bot):
    data = [
        (
            [
                BotCommand(command="start", description="Начало работы"),
                BotCommand(command="help", description="Описание режимов работы"),
            ],
            BotCommandScopeAllPrivateChats(),
            None,
        )
    ]

    for commands_list, commands_scope, language in data:
        await bot.set_my_commands(
            commands=commands_list, scope=commands_scope, language_code=language
        )
