from aiogram import F, Router, types, exceptions
from aiogram.filters import Command

from bot_app.modules import messages
from bot_app.tg.keyboards.manager import start_and_manager
from bot_app.tg.callbacks.lessons import HelpData


help_router = Router()


@help_router.message(Command(commands=["help"]))
async def get_help(message: types.Message | types.CallbackQuery):
    try:
        await message.edit_text(messages.HELP_MESSAGE, reply_markup=start_and_manager())
    except exceptions.TelegramBadRequest as error:
        await message.answer(messages.HELP_MESSAGE, reply_markup=start_and_manager())


@help_router.callback_query(HelpData.filter())
async def get_back_lessons(callback: types.CallbackQuery, callback_data: HelpData):

    await callback.answer()
    await callback.message.edit_text(
        messages.HELP_MESSAGE, reply_markup=start_and_manager()
    )
