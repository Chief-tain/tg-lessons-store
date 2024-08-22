import logging

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot_app.application.user_service import UserService
from bot_app.application.lesson_service import LessonService
from bot_app.application.payment_service import PaymentService
from bot_app.modules import messages
from bot_app.tg.states.states import States
import bot_app.tg.keyboards.lessons as lessons_kb
from bot_app.tg.callbacks.lessons import Lessondata, BuyLessonData, BackData


lessons_router = Router()


@lessons_router.message(Command(commands=["lessons"]))
async def get_lessons(message: types.Message, lesson_service: LessonService):

    lessons = await lesson_service.get_lessons()
    await message.answer(
        text=messages.LESSONS_MESSAGE, reply_markup=lessons_kb.lessons(lessons=lessons)
    )


@lessons_router.callback_query(BackData.filter())
async def get_back_lessons(
    callback: types.CallbackQuery,
    callback_data: BackData,
    lesson_service: LessonService,
):

    await callback.answer()
    lessons = await lesson_service.get_lessons()

    await callback.message.edit_text(
        text=messages.LESSONS_MESSAGE, reply_markup=lessons_kb.lessons(lessons=lessons)
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
