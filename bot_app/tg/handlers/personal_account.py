import logging

from aiogram import F, Router, types, exceptions
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot_app.application.user_service import UserService
from bot_app.application.lesson_service import LessonService
from bot_app.application.minio_service import OrderMediaRepository
from bot_app.modules import messages
from bot_app.tg.states.states import States
import bot_app.tg.keyboards.lessons as lessons_kb
from bot_app.tg.callbacks.lessons import (
    Lessondata,
    BuyLessonData,
    BackData,
    EnglishModeDaata,
    ChineseModeData,
    ChooseModeData,
    TotalBackData,
    GetDemoData,
    PersonalAccountData,
)
from shared.settings import S3_BUCKET
from shared.models import Users


personal_account_router = Router()


@personal_account_router.message(Command(commands=["personal_account"]))
async def personal_account_func(
    message: types.Message, user_service: UserService, state: FSMContext
):
    user: Users = await user_service.get_user(user_id=message.from_user.id)

    await message.answer(
        text=messages.PERSONAL_ACCOUNT_MESSAGE.format(
            username=user.username,
            language_code=user.language_code,
            registered_at=(str(user.registered_at))[:11],
            bouhgt_amount=len(user.bought_lessons_id),
        )
    )


@personal_account_router.callback_query(PersonalAccountData.filter())
async def personal_account_func(
    callback: types.CallbackQuery,
    callback_data: PersonalAccountData,
    user_service: UserService,
    lesson_service: LessonService,
    state: FSMContext,
):
    await callback.answer()

    user: Users = await user_service.get_user(user_id=callback.from_user.id)

    await callback.message.answer(
        text=messages.PERSONAL_ACCOUNT_MESSAGE.format(
            username=user.username,
            language_code=user.language_code,
            registered_at=(str(user.registered_at))[:11],
            bouhgt_amount=len(user.bought_lessons_id),
        )
    )
