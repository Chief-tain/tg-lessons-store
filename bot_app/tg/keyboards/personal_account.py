from aiogram.utils.keyboard import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot_app.tg.callbacks.lessons import (
    HelpData,
    BoughtLessonData,
)

import bot_app.modules.messages as messages
from shared.settings import SUPPORT_ACCOUNT
from shared.models import Lessons


def get_lessons_buttons(lessons: list[Lessons]):

    keyboard = [
        [
            InlineKeyboardButton(
                text=f"{messages.language_smile[lesson.language]} {lesson.name} - {int(lesson.price)}₽ ✅",
                callback_data=BoughtLessonData(lesson_id=lesson.id).pack(),
            )
        ]
        for lesson in lessons
    ]
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
