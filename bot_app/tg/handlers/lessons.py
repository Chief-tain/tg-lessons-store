import logging

from aiogram import F, Router, types, exceptions
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot_app.application.user_service import UserService
from bot_app.application.lesson_service import LessonService
from bot_app.application.payment_service import PaymentService
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
)


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

    try:
        await message.edit_text(
            text=messages.LESSONS_MESSAGE,
            reply_markup=lessons_kb.lessons(lessons=lessons, language="en"),
        )
    except exceptions.TelegramBadRequest as error:
        await message.answer(
            text=messages.LESSONS_MESSAGE,
            reply_markup=lessons_kb.lessons(lessons=lessons, language="en"),
        )
    await state.set_data({"language": "en"})


@lessons_router.callback_query(EnglishModeDaata.filter())
async def get_en_lessons(
    callback: types.CallbackQuery, lesson_service: LessonService, state: FSMContext
):
    await callback.answer()
    lessons = await lesson_service.get_lessons(language="en")
    await callback.message.edit_text(
        text=messages.LESSONS_MESSAGE,
        reply_markup=lessons_kb.lessons(lessons=lessons, language="en"),
    )
    await state.set_data({"language": "en"})


@lessons_router.message(Command(commands=["chinese_lessons"]))
async def get_en_lessons(
    message: types.Message, lesson_service: LessonService, state: FSMContext
):
    lessons = await lesson_service.get_lessons(language="zh")

    try:
        await message.edit_text(
            text=messages.LESSONS_MESSAGE,
            reply_markup=lessons_kb.lessons(lessons=lessons, language="zh"),
        )
    except exceptions.TelegramBadRequest as error:
        await message.answer(
            text=messages.LESSONS_MESSAGE,
            reply_markup=lessons_kb.lessons(lessons=lessons, language="zh"),
        )

    await state.set_data({"language": "zh"})


@lessons_router.callback_query(ChineseModeData.filter())
async def get_en_lessons(
    callback: types.CallbackQuery, lesson_service: LessonService, state: FSMContext
):
    await callback.answer()
    lessons = await lesson_service.get_lessons(language="zh")
    await callback.message.edit_text(
        text=messages.LESSONS_MESSAGE,
        reply_markup=lessons_kb.lessons(lessons=lessons, language="zh"),
    )
    await state.set_data({"language": "zh"})


@lessons_router.callback_query(BackData.filter())
async def get_back_lessons(
    callback: types.CallbackQuery,
    callback_data: BackData,
    lesson_service: LessonService,
    state: FSMContext,
):
    await callback.answer()
    language = (await state.get_data())["language"]
    lessons = await lesson_service.get_lessons(language=language)

    await callback.message.edit_text(
        text=messages.LESSONS_MESSAGE,
        reply_markup=lessons_kb.lessons(lessons=lessons, language=language),
    )


@lessons_router.callback_query(Lessondata.filter())
async def get_lesson(
    callback: types.CallbackQuery,
    callback_data: Lessondata,
    lesson_service: LessonService,
):
    await callback.answer()
    lesson = await lesson_service.get_lesson(lesson_id=callback_data.lesson_id)

    await callback.message.edit_text(
        text=messages.LESSON_DETAILS_MESSAGE.format(
            name=lesson.name, description=lesson.description, price=int(lesson.price)
        ),
        reply_markup=lessons_kb.lesson(lesson=lesson),
    )
