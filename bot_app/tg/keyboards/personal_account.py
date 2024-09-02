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
    NullData,
)

from shared.models import Lessons


language_smile = {"en": "🇬🇧", "zh": "🇨🇳"}


def get_lessons_buttons(lessons: list[Lessons]):

    keyboard = [
        [
            InlineKeyboardButton(
                text=f"{language_smile[lesson.language]} {lesson.name} - {int(lesson.price)}₽ ✅",
                callback_data=NullData().pack(),
            )
        ]
        for lesson in lessons
    ]
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
