from math import ceil

from aiogram.utils.keyboard import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot_app.tg.callbacks.lessons import (
    AdminLessondata,
    AdminPaginationData,
    AddLessonData,
    EditLessonData,
    AdminBackData,
)

import bot_app.modules.messages as messages
from shared.models import Lessons
from shared.settings import SUPPORT_ACCOUNT


def get_all_lessons(lessons: list[Lessons], limit: int = 7, offset: int = 0):
    keyboard = []

    for lesson in lessons[offset : offset + limit]:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"{messages.language_smile[lesson.language]} {lesson.name} - {int(lesson.price)}₽ - {'✅' if lesson.is_available else '❌'}",
                    callback_data=AdminLessondata(lesson_id=lesson.id).pack(),
                )
            ]
        )
    if len(lessons) > limit:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text="<",
                    callback_data=AdminPaginationData(direction="prev").pack(),
                ),
                InlineKeyboardButton(
                    text=f"[{offset // limit + 1}/{ceil(len(lessons) / limit)}]",
                    callback_data=AdminPaginationData(direction="keep").pack(),
                ),
                InlineKeyboardButton(
                    text=">",
                    callback_data=AdminPaginationData(direction="next").pack(),
                ),
            ]
        )
    keyboard.append(
        [
            InlineKeyboardButton(
                text=messages.ADD_LESSON_MESSAGE,
                callback_data=AddLessonData().pack(),
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard, resize_keyboard=True)


def get_admin_lesson(lesson: Lessons):
    keyboard = [
        [
            InlineKeyboardButton(
                text="🇬🇧 Язык (en, zh) 🇨🇳",
                callback_data=EditLessonData(feature="language").pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="🌻 Название 🌻",
                callback_data=EditLessonData(feature="name").pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="🚀 Описание 🚀",
                callback_data=EditLessonData(feature="description").pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="📸 Изображение 📸",
                callback_data=EditLessonData(feature="photo_url").pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="📄 Демо-файлы 📄",
                callback_data=EditLessonData(feature="demo_urls").pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="📚 Основные файлы 📚",
                callback_data=EditLessonData(feature="doc_urls").pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="💵 Цена 💵",
                callback_data=EditLessonData(feature="price").pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="✅ Активность ❌",
                callback_data=EditLessonData(feature="is_available").pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text=messages.BACK_MESSAGE,
                callback_data=AdminBackData().pack(),
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard, resize_keyboard=True)
