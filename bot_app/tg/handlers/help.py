from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot_app.modules import messages
from bot_app.tg.states.states import States
from bot_app.tg.keyboards.manager import manager
from bot_app.tg.callbacks.lessons import HelpData


help_router = Router()


@help_router.message(Command(commands=["help"]))
async def get_help(message: types.Message | types.CallbackQuery, state: FSMContext):
    await message.answer(messages.HELP_MESSAGE, reply_markup=manager())


@help_router.callback_query(HelpData.filter())
async def get_back_lessons(callback: types.CallbackQuery, callback_data: HelpData):

    await callback.answer()
    await callback.message.answer(messages.HELP_MESSAGE, reply_markup=manager())
