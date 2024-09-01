from aiogram.utils.keyboard import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot_app.tg.callbacks.lessons import (
    HelpData,
    BackData,
    ChooseModeData,
    PersonalAccountData,
)


def start_and_manager():
    keyboard = [
        [
            InlineKeyboardButton(
                text=f"✅ Начать ✅",
                callback_data=ChooseModeData().pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text=f"🧍‍♂ Личный кабинет 🧍‍♀",
                callback_data=PersonalAccountData().pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="🆘 Служба поддержки 🆘",
                url="https://t.me/Chief_train",  # todo: emplace
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard, resize_keyboard=True)


def start_and_manager_and_help():
    keyboard = [
        [
            InlineKeyboardButton(
                text=f"✅ Начать ✅",
                callback_data=ChooseModeData().pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text=f"🧍‍♂ Личный кабинет 🧍‍♀",
                callback_data=PersonalAccountData().pack(),
            )
        ],
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
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard, resize_keyboard=True)
