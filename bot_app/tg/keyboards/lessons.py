from math import ceil

from aiogram.utils.keyboard import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot_app.tg.callbacks.lessons import (
    Lessondata,
    BackData,
    BuyLessonData,
    HelpData,
    ChineseModeData,
    EnglishModeDaata,
    TotalBackData,
    GetDemoData,
    PersonalAccountData,
    PaginationData,
)

import bot_app.modules.messages as messages
from shared.models import Lessons
from shared.settings import SUPPORT_ACCOUNT


def choose_lang_mode():
    keyboard = [
        [
            InlineKeyboardButton(
                text=messages.ENGLISH_LANGUAHE_MESSAGE,
                callback_data=EnglishModeDaata().pack(),
            ),
            InlineKeyboardButton(
                text=messages.CHINESE_LANGUAGE_MESSAGE,
                callback_data=ChineseModeData().pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text=messages.PA_MESSAGE,
                callback_data=PersonalAccountData().pack(),
            )
        ],
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
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard, resize_keyboard=True)


def lessons(lessons: list[Lessons], language: str, limit: int = 7, offset: int = 0):
    keyboard = []

    for lesson in lessons[offset : offset + limit]:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"{messages.language_smile[language]} {lesson.name} - {int(lesson.price)}₽",
                    callback_data=Lessondata(lesson_id=lesson.id).pack(),
                )
            ]
        )
    if len(lessons) > limit:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text="<",
                    callback_data=PaginationData(direction="prev").pack(),
                ),
                InlineKeyboardButton(
                    text=f"[{offset // limit + 1}/{ceil(len(lessons) / limit)}]",
                    callback_data=PaginationData(direction="keep").pack(),
                ),
                InlineKeyboardButton(
                    text=">",
                    callback_data=PaginationData(direction="next").pack(),
                ),
            ]
        )
    keyboard.append(
        [
            InlineKeyboardButton(
                text=messages.BACK_MESSAGE,
                callback_data=TotalBackData().pack(),
            )
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


def lesson(lesson: Lessons):

    keyboard = [
        [
            InlineKeyboardButton(
                text=messages.DEMO_VERSION_MESSAGE,
                callback_data=GetDemoData(lesson_id=lesson.id).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text=messages.BACK_MESSAGE,
                callback_data=BackData().pack(),
            ),
            InlineKeyboardButton(
                text=messages.BUY_MESSAGE,
                callback_data=BuyLessonData(lesson_id=lesson.id).pack(),
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard, resize_keyboard=True)
