from aiogram import F, Router, types
from aiogram.filters import Command

from bot_app.application.user_service import UserService
from bot_app.application.lesson_service import LessonService
from bot_app.application.minio_service import OrderMediaRepository
from bot_app.modules import messages
import bot_app.tg.keyboards.personal_account as account_kb
from bot_app.tg.callbacks.lessons import PersonalAccountData, BoughtLessonData
from shared.settings import S3_BUCKET
from shared.models import Users, Lessons


personal_account_router = Router()


@personal_account_router.message(Command(commands=["personal_account"]))
async def personal_account_func(
    message: types.Message,
    user_service: UserService,
    lesson_service: LessonService,
):
    user: Users = await user_service.get_user(user_id=message.from_user.id)
    bought_lessons_ids: list[int] = user.bought_lessons_id
    lessons_list: list[Lessons] = [
        (await lesson_service.get_lesson(lesson_id=current_id))
        for current_id in bought_lessons_ids
    ]

    await message.answer(
        text=messages.PERSONAL_ACCOUNT_MESSAGE.format(
            username=user.username,
            language_code=user.language_code,
            registered_at=(str(user.registered_at))[:11],
            bouhgt_amount=len(user.bought_lessons_id),
        ),
        reply_markup=account_kb.get_lessons_buttons(lessons=lessons_list),
    )


@personal_account_router.callback_query(PersonalAccountData.filter())
async def personal_account_func(
    callback: types.CallbackQuery,
    user_service: UserService,
    lesson_service: LessonService,
):
    await callback.answer()

    user: Users = await user_service.get_user(user_id=callback.from_user.id)
    bought_lessons_ids: list[int] = user.bought_lessons_id
    lessons_list: list[Lessons] = [
        (await lesson_service.get_lesson(lesson_id=current_id))
        for current_id in bought_lessons_ids
    ]

    await callback.message.edit_text(
        text=messages.PERSONAL_ACCOUNT_MESSAGE.format(
            username=user.username,
            language_code=user.language_code,
            registered_at=(str(user.registered_at))[:11],
            bouhgt_amount=len(user.bought_lessons_id),
        ),
        reply_markup=account_kb.get_lessons_buttons(lessons=lessons_list),
    )


@personal_account_router.callback_query(BoughtLessonData.filter())
async def get_bought_lesson(
    callback: types.CallbackQuery,
    callback_data: BoughtLessonData,
    user_service: UserService,
    lesson_service: LessonService,
    order_media_minio: OrderMediaRepository,
):
    await callback.answer()

    lesson = await lesson_service.get_lesson(lesson_id=callback_data.lesson_id)

    for i in range(1, 4):
        await callback.message.answer(text=f"Документ №{i} из урока {lesson.name}")
