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
import bot_app.modules.messages as messages
from shared.settings import SUPPORT_ACCOUNT


def start_and_manager():
    keyboard = [
        [
            InlineKeyboardButton(
                text=messages.BEGIN_MESSAGE,
                callback_data=ChooseModeData().pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text=messages.PA_MESSAGE,
                callback_data=PersonalAccountData().pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text=messages.SUPPORT_MESSAGE,
                url=SUPPORT_ACCOUNT,
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard, resize_keyboard=True)


def start_and_manager_and_help():
    keyboard = [
        [
            InlineKeyboardButton(
                text=messages.BEGIN_MESSAGE,
                callback_data=ChooseModeData().pack(),
            )
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
                url=SUPPORT_ACCOUNT,  # todo: emplace
            ),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard, resize_keyboard=True)
