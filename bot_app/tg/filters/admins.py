from aiogram.filters import BaseFilter
from aiogram.types import Message

from shared.settings import ADMINS_TG_ID


class OnlyAdminsFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.from_user.id in ADMINS_TG_ID:
            return True

        return False
