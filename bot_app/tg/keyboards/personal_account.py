from math import ceil
from aiogram.utils.keyboard import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot_app.tg.callbacks.lessons import HelpData, BoughtLessonData, PAPaginationData
import bot_app.modules.messages as messages

from shared.settings import SUPPORT_ACCOUNT
from shared.models import Lessons


def get_lessons_buttons(lessons: list[Lessons], limit: int = 7, offset: int = 0):
    keyboard = []

    for lesson in lessons[offset : offset + limit]:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"{messages.language_smile[lesson.language]} {lesson.name} - {int(lesson.price)}₽ ✅",
                    callback_data=BoughtLessonData(lesson_id=lesson.id).pack(),
                )
            ]
        )
    if len(lessons) > limit:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text="<",
                    callback_data=PAPaginationData(direction="prev").pack(),
                ),
                InlineKeyboardButton(
                    text=f"[{offset // limit + 1}/{ceil(len(lessons) / limit)}]",
                    callback_data=PAPaginationData(direction="keep").pack(),
                ),
                InlineKeyboardButton(
                    text=">",
                    callback_data=PAPaginationData(direction="next").pack(),
                ),
            ]
        )
    keyboard.append(
        [
            InlineKeyboardButton(
                text=messages.QUESTIONS_MESSAGE,
                callback_data=HelpData().pack(),
            ),
            InlineKeyboardButton(
                text=messages.SUPPORT_MESSAGE,
                url=SUPPORT_ACCOUNT,
            ),
        ],
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard, resize_keyboard=True)
