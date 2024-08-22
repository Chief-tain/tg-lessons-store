from aiogram.utils.keyboard import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot_app.tg.callbacks.lessons import Lessondata, BackData, BuyLessonData, HelpData

from shared.models import Lessons


def lessons(lessons: list[Lessons]):

    keyboard = [
        [
            InlineKeyboardButton(
                text=f"🇨🇳 {lesson.name} - {int(lesson.price)}₽",
                callback_data=Lessondata(lesson_id=lesson.id).pack(),
            )
        ]
        for lesson in lessons
    ]
    keyboard.append(
        [
            InlineKeyboardButton(
                text=f"❓ Ответы на вопросы ❓",
                callback_data=HelpData().pack(),
            ),
            InlineKeyboardButton(
                text="🆘 Служба поддержки 🆘",
                url="https://t.me/Chief_train",  # todo: emplace
            ),
        ],
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard, resize_keyboard=True)


def lesson(lesson: Lessons):

    keyboard = [
        [
            InlineKeyboardButton(
                text=f"🔙 Назад 🔙",
                callback_data=BackData().pack(),
            ),
            InlineKeyboardButton(
                text=f"✅ Купить ✅",
                callback_data=BuyLessonData(lesson_id=lesson.id).pack(),
            ),
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard, resize_keyboard=True)
