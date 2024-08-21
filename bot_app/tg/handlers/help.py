from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot_app.modules import messages
from bot_app.tg.states.start import StartState


help_router = Router()


@help_router.message(Command(commands=["help"]))
@help_router.callback_query(StartState.help)
async def get_help(message: types.Message, state: FSMContext):
    await message.answer(messages.HELP_MESSAGE)
