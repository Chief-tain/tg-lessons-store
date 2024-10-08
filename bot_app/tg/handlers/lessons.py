from aiogram import F, Router, types, exceptions
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot_app.application.lesson_service import LessonService
from bot_app.application.minio_service import OrderMediaRepository
from bot_app.modules import messages
import bot_app.tg.keyboards.lessons as lessons_kb
from bot_app.tg.callbacks.lessons import (
    Lessondata,
    BackData,
    EnglishModeDaata,
    ChineseModeData,
    ChooseModeData,
    PaginationData,
    TotalBackData,
    GetDemoData,
)
from shared.settings import S3_BUCKET

START_LIMIT: int = 7
START_OFFSET: int = 0

lessons_router = Router()


@lessons_router.message(Command(commands=["lessons"]))
async def choose_lessons_mode(message: types.Message):
    await message.answer(
        text=messages.LESSONS_MODE_MESSAGE, reply_markup=lessons_kb.choose_lang_mode()
    )


@lessons_router.callback_query(TotalBackData.filter())
@lessons_router.callback_query(ChooseModeData.filter())
async def choose_lessons_mode(callback: types.CallbackQuery):
    await callback.answer()

    await callback.message.edit_text(
        text=messages.LESSONS_MODE_MESSAGE, reply_markup=lessons_kb.choose_lang_mode()
    )


@lessons_router.message(Command(commands=["english_lessons"]))
async def get_en_lessons(
    message: types.Message, lesson_service: LessonService, state: FSMContext
):
    lessons = await lesson_service.get_lessons(language="en")

    limit = START_LIMIT
    offset = START_OFFSET
    await state.update_data({"limit": limit, "offset": offset, "language": "en"})

    try:
        await message.edit_text(
            text=messages.LESSONS_MESSAGE,
            reply_markup=lessons_kb.lessons(
                lessons=lessons, language="en", limit=limit, offset=offset
            ),
        )
    except exceptions.TelegramBadRequest as error:
        await message.answer(
            text=messages.LESSONS_MESSAGE,
            reply_markup=lessons_kb.lessons(
                lessons=lessons, language="en", limit=limit, offset=offset
            ),
        )


@lessons_router.callback_query(EnglishModeDaata.filter())
async def get_en_lessons(
    callback: types.CallbackQuery, lesson_service: LessonService, state: FSMContext
):
    await callback.answer()
    lessons = await lesson_service.get_lessons(language="en")

    limit = START_LIMIT
    offset = START_OFFSET
    await state.update_data({"limit": limit, "offset": offset, "language": "en"})

    await callback.message.edit_text(
        text=messages.LESSONS_MESSAGE,
        reply_markup=lessons_kb.lessons(
            lessons=lessons, language="en", limit=limit, offset=offset
        ),
    )


@lessons_router.message(Command(commands=["chinese_lessons"]))
async def get_en_lessons(
    message: types.Message, lesson_service: LessonService, state: FSMContext
):
    lessons = await lesson_service.get_lessons(language="zh")

    limit = START_LIMIT
    offset = START_OFFSET
    await state.update_data({"limit": limit, "offset": offset, "language": "zh"})

    try:
        await message.edit_text(
            text=messages.LESSONS_MESSAGE,
            reply_markup=lessons_kb.lessons(
                lessons=lessons, language="zh", limit=limit, offset=offset
            ),
        )
    except exceptions.TelegramBadRequest as error:
        await message.answer(
            text=messages.LESSONS_MESSAGE,
            reply_markup=lessons_kb.lessons(
                lessons=lessons, language="zh", limit=limit, offset=offset
            ),
        )


@lessons_router.callback_query(ChineseModeData.filter())
async def get_en_lessons(
    callback: types.CallbackQuery, lesson_service: LessonService, state: FSMContext
):
    await callback.answer()
    lessons = await lesson_service.get_lessons(language="zh")

    limit = START_LIMIT
    offset = START_OFFSET
    await state.update_data({"limit": limit, "offset": offset, "language": "zh"})

    await callback.message.edit_text(
        text=messages.LESSONS_MESSAGE,
        reply_markup=lessons_kb.lessons(
            lessons=lessons, language="zh", limit=limit, offset=offset
        ),
    )


@lessons_router.callback_query(BackData.filter())
async def get_back_lessons(
    callback: types.CallbackQuery,
    callback_data: BackData,
    lesson_service: LessonService,
    state: FSMContext,
):
    await callback.answer()

    data = await state.get_data()
    offset = data["offset"]
    limit = data["limit"]
    language = data["language"]

    lessons = await lesson_service.get_lessons(language=language)

    await callback.message.delete()
    await callback.message.answer(
        text=messages.LESSONS_MESSAGE,
        reply_markup=lessons_kb.lessons(
            lessons=lessons, language=language, limit=limit, offset=offset
        ),
    )


@lessons_router.callback_query(PaginationData.filter())
async def channel_navigation(
    callback: types.CallbackQuery,
    callback_data: PaginationData,
    state: FSMContext,
    lesson_service: LessonService,
):
    await callback.answer()
    data = await state.get_data()
    offset = data["offset"]
    limit = data["limit"]
    language = data["language"]

    lessons = await lesson_service.get_lessons(language=language)

    if callback_data.direction == "prev":
        if offset == 0:
            return
        offset -= limit
        await state.update_data({"offset": offset})
        await callback.message.edit_reply_markup(
            reply_markup=lessons_kb.lessons(
                lessons=lessons, language=language, limit=limit, offset=offset
            )
        )
    if callback_data.direction == "next":
        if offset + limit >= len(lessons):
            return
        offset += limit

        await state.update_data({"offset": offset})
        await callback.message.edit_reply_markup(
            reply_markup=lessons_kb.lessons(
                lessons=lessons, language=language, limit=limit, offset=offset
            )
        )


@lessons_router.callback_query(Lessondata.filter())
async def get_lesson(
    callback: types.CallbackQuery,
    callback_data: Lessondata,
    lesson_service: LessonService,
    order_media_minio: OrderMediaRepository,
):
    await callback.answer()
    lesson = await lesson_service.get_lesson(lesson_id=callback_data.lesson_id)

    media, metadata = await order_media_minio.get_safe_objects_by_name(
        bucket_id=S3_BUCKET, object_name=lesson.photo_url
    )

    await callback.message.delete()
    await callback.message.answer_photo(
        photo=types.BufferedInputFile(file=media, filename="picture"),
        caption=messages.LESSON_DETAILS_MESSAGE.format(
            name=lesson.name, description=lesson.description, price=int(lesson.price)
        ),
        reply_markup=lessons_kb.lesson(lesson=lesson),
    )


@lessons_router.callback_query(GetDemoData.filter())
async def get_demo(
    callback: types.CallbackQuery,
    callback_data: GetDemoData,
    lesson_service: LessonService,
    order_media_minio: OrderMediaRepository,
):
    await callback.answer()
    lesson = await lesson_service.get_lesson(lesson_id=callback_data.lesson_id)

    await callback.message.answer(
        text=messages.WAIT_FOR_SENDING_MESSAGE.format(name=lesson.name)
    )

    for demo_url in lesson.demo_urls:
        media, metadata = await order_media_minio.get_safe_objects_by_name(
            bucket_id=S3_BUCKET, object_name=demo_url
        )
        await callback.message.answer_document(
            document=types.BufferedInputFile(file=media, filename=demo_url),
        )
