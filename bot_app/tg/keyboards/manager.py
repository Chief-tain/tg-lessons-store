from aiogram.utils.keyboard import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot_app.tg.callbacks.lessons import HelpData, BackData


def manager():
    keyboard = [
        [
            InlineKeyboardButton(
                text="🆘 Служба поддержки 🆘",
                url="https://t.me/Chief_train",  # todo: emplace
            )
        ],
        [
            InlineKeyboardButton(
                text=f"✅ Начать ✅",
                callback_data=BackData().pack(),
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard, resize_keyboard=True)


def manager_and_help():
    keyboard = [
        [
            InlineKeyboardButton(
                text=f"✅ Начать ✅",
                callback_data=BackData().pack(),
            )
        ],
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
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard, resize_keyboard=True)
