import logging

from aiogram import F, Router, types, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot_app.tg.filters.admins import OnlyAdminsFilter

moderator_router = Router()


@moderator_router.message(Command(commands="admin"), OnlyAdminsFilter())
async def get_moderate_kb(
    message: types.Message,
    state: FSMContext,
):
    logging.info("Get moderate keyboards")

    await message.answer(
        text="Привет, администратор!",
    )
