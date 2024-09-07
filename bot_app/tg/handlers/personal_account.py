from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot_app.application.user_service import UserService
from bot_app.application.lesson_service import LessonService
from bot_app.application.minio_service import OrderMediaRepository
from bot_app.modules import messages
import bot_app.tg.keyboards.personal_account as account_kb
from bot_app.tg.callbacks.lessons import (
    PersonalAccountData,
    BoughtLessonData,
    PAPaginationData,
)
from shared.settings import S3_BUCKET
from shared.models import Users, Lessons

START_LIMIT: int = 7
START_OFFSET: int = 0


personal_account_router = Router()


@personal_account_router.message(Command(commands=["personal_account"]))
async def personal_account_func(
    message: types.Message,
    user_service: UserService,
    lesson_service: LessonService,
    state: FSMContext,
):
    user: Users = await user_service.get_user(user_id=message.from_user.id)
    bought_lessons_ids: list[int] = user.bought_lessons_id
    lessons_list: list[Lessons] = [
        (await lesson_service.get_lesson(lesson_id=current_id))
        for current_id in bought_lessons_ids
    ]

    pa_limit = START_LIMIT
    pa_offset = START_OFFSET

    await state.update_data({"pa_limit": pa_limit, "pa_offset": pa_offset})

    await message.answer(
        text=messages.PERSONAL_ACCOUNT_MESSAGE.format(
            username=user.username,
            language_code=user.language_code,
            registered_at=(str(user.registered_at))[:11],
            bouhgt_amount=len(user.bought_lessons_id),
        ),
        reply_markup=account_kb.get_lessons_buttons(
            lessons=lessons_list, limit=pa_limit, offset=pa_offset
        ),
    )


@personal_account_router.callback_query(PersonalAccountData.filter())
async def personal_account_func(
    callback: types.CallbackQuery,
    user_service: UserService,
    lesson_service: LessonService,
    state: FSMContext,
):
    await callback.answer()

    user: Users = await user_service.get_user(user_id=callback.from_user.id)
    bought_lessons_ids: list[int] = user.bought_lessons_id
    lessons_list: list[Lessons] = [
        (await lesson_service.get_lesson(lesson_id=current_id))
        for current_id in bought_lessons_ids
    ]

    pa_limit = START_LIMIT
    pa_offset = START_OFFSET

    await state.update_data({"pa_limit": pa_limit, "pa_offset": pa_offset})

    await callback.message.edit_text(
        text=messages.PERSONAL_ACCOUNT_MESSAGE.format(
            username=user.username,
            language_code=user.language_code,
            registered_at=(str(user.registered_at))[:11],
            bouhgt_amount=len(user.bought_lessons_id),
        ),
        reply_markup=account_kb.get_lessons_buttons(
            lessons=lessons_list, limit=pa_limit, offset=pa_offset
        ),
    )


@personal_account_router.callback_query(PAPaginationData.filter())
async def channel_navigation(
    callback: types.CallbackQuery,
    callback_data: PAPaginationData,
    state: FSMContext,
    lesson_service: LessonService,
    user_service: UserService,
):
    await callback.answer()
    data = await state.get_data()
    pa_offset = data["pa_offset"]
    pa_limit = data["pa_limit"]

    user: Users = await user_service.get_user(user_id=callback.from_user.id)
    bought_lessons_ids: list[int] = user.bought_lessons_id
    lessons_list: list[Lessons] = [
        (await lesson_service.get_lesson(lesson_id=current_id))
        for current_id in bought_lessons_ids
    ]

    if callback_data.direction == "prev":
        if pa_offset == 0:
            return
        pa_offset -= pa_limit
        await state.update_data({"pa_offset": pa_offset})
        await callback.message.edit_reply_markup(
            reply_markup=account_kb.get_lessons_buttons(
                lessons=lessons_list, limit=pa_limit, offset=pa_offset
            )
        )
    if callback_data.direction == "next":
        if pa_offset + pa_limit >= len(lessons_list):
            return
        pa_offset += pa_limit

        await state.update_data({"pa_offset": pa_offset})
        await callback.message.edit_reply_markup(
            reply_markup=account_kb.get_lessons_buttons(
                lessons=lessons_list, limit=pa_limit, offset=pa_offset
            )
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

    await callback.message.answer(
        text=messages.WAIT_FOR_SENDING_MESSAGE.format(name=lesson.name)
    )

    for doc_url in lesson.doc_urls:
        media, metadata = await order_media_minio.get_safe_objects_by_name(
            bucket_id=S3_BUCKET, object_name=doc_url
        )
        await callback.message.answer_document(
            document=types.BufferedInputFile(file=media, filename=doc_url),
            protect_content=True,
        )
