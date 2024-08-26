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
)

from shared.models import Lessons


language_smile = {"en": "🇬🇧", "zh": "🇨🇳"}


def choose_lang_mode():
    keyboard = [
        [
            InlineKeyboardButton(
                text=f"🇬🇧 Английский 🇬🇧",
                callback_data=EnglishModeDaata().pack(),
            ),
            InlineKeyboardButton(
                text=f"🇨🇳 Китайский 🇨🇳",
                callback_data=ChineseModeData().pack(),
            ),
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard, resize_keyboard=True)


def lessons(lessons: list[Lessons], language: str):

    keyboard = [
        [
            InlineKeyboardButton(
                text=f"{language_smile[language]} {lesson.name} - {int(lesson.price)}₽",
                callback_data=Lessondata(lesson_id=lesson.id).pack(),
            )
        ]
        for lesson in lessons
    ]
    keyboard.append(
        [
            InlineKeyboardButton(
                text=f"🔙 Назад 🔙",
                callback_data=TotalBackData().pack(),
            )
        ]
    )
    keyboard.append(
        [
            InlineKeyboardButton(
                text=f"❓ Вопросы ❓",
                callback_data=HelpData().pack(),
            ),
            InlineKeyboardButton(
                text="🆘 Поддержка 🆘",
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
