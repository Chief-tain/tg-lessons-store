from aiogram.filters.callback_data import CallbackData


class Lessondata(CallbackData, prefix="lesson"):
    lesson_id: int


class BackData(CallbackData, prefix="back"):
    pass


class BuyLessonData(CallbackData, prefix="buy"):
    lesson_id: int


class HelpData(CallbackData, prefix="help"):
    pass
