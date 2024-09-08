import logging

from aiogram import F, Router, types, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import bot_app.tg.keyboards.moderator as moderator_kb
from bot_app.tg.filters.admins import OnlyAdminsFilter
from bot_app.application.lesson_service import LessonService
from bot_app.application.minio_service import OrderMediaRepository
from bot_app.modules import messages
from bot_app.tg.callbacks.lessons import (
    AdminPaginationData,
    AdminLessondata,
    AdminBackData,
)

START_LIMIT: int = 7
START_OFFSET: int = 0


moderator_router = Router()


@moderator_router.message(Command(commands="admin"), OnlyAdminsFilter())
async def get_moderate_kb(
    message: types.Message,
    state: FSMContext,
    lesson_service: LessonService,
):
    all_lessons = await lesson_service.get_all_lessons()

    admin_limit = START_LIMIT
    admin_offset = START_OFFSET
    await state.update_data({"admin_limit": admin_limit, "admin_offset": admin_offset})

    await message.answer(
        text=messages.ADMIN_START_MESSAGE.format(name=message.from_user.username),
        reply_markup=moderator_kb.get_all_lessons(
            lessons=all_lessons, limit=admin_limit, offset=admin_offset
        ),
    )


@moderator_router.callback_query(AdminBackData.filter())
async def get_moderate_kb(
    callback: types.CallbackQuery,
    state: FSMContext,
    lesson_service: LessonService,
):
    all_lessons = await lesson_service.get_all_lessons()

    await callback.answer()
    data = await state.get_data()
    admin_offset = data["admin_offset"]
    admin_limit = data["admin_limit"]

    await callback.message.edit_text(
        text=messages.ADMIN_START_MESSAGE.format(name=callback.from_user.username),
        reply_markup=moderator_kb.get_all_lessons(
            lessons=all_lessons, limit=admin_limit, offset=admin_offset
        ),
    )


@moderator_router.callback_query(AdminPaginationData.filter())
async def admin_navigation(
    callback: types.CallbackQuery,
    callback_data: AdminPaginationData,
    state: FSMContext,
    lesson_service: LessonService,
):
    await callback.answer()
    data = await state.get_data()
    admin_offset = data["admin_offset"]
    admin_limit = data["admin_limit"]

    all_lessons = await lesson_service.get_all_lessons()

    if callback_data.direction == "prev":
        if admin_offset == 0:
            return
        admin_offset -= admin_limit
        await state.update_data({"admin_offset": admin_offset})
        await callback.message.edit_reply_markup(
            reply_markup=moderator_kb.get_all_lessons(
                lessons=all_lessons, limit=admin_limit, offset=admin_offset
            )
        )
    if callback_data.direction == "next":
        if admin_offset + admin_limit >= len(all_lessons):
            return
        admin_offset += admin_limit

        await state.update_data({"admin_offset": admin_offset})
        await callback.message.edit_reply_markup(
            reply_markup=moderator_kb.get_all_lessons(
                lessons=all_lessons, limit=admin_limit, offset=admin_offset
            )
        )


@moderator_router.callback_query(AdminLessondata.filter())
async def admin_lesson(
    callback: types.CallbackQuery,
    callback_data: AdminLessondata,
    state: FSMContext,
    lesson_service: LessonService,
):
    lesson = await lesson_service.get_lesson(lesson_id=callback_data.lesson_id)

    await callback.message.edit_text(
        text=messages.EDIT_LESSON_MESSAGE,
        reply_markup=moderator_kb.get_admin_lesson(lesson=lesson),
    )
