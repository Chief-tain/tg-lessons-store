from aiogram.filters.callback_data import CallbackData


class NullData(CallbackData, prefix="null"):
    pass


class BoughtLessonData(CallbackData, prefix="bought_lesson"):
    lesson_id: int


class Lessondata(CallbackData, prefix="lesson"):
    lesson_id: int


class BackData(CallbackData, prefix="back"):
    pass


class TotalBackData(CallbackData, prefix="total_back"):
    pass


class BuyLessonData(CallbackData, prefix="buy"):
    lesson_id: int


class HelpData(CallbackData, prefix="help"):
    pass


class ChooseModeData(CallbackData, prefix="choose"):
    pass


class EnglishModeDaata(CallbackData, prefix="english"):
    pass


class ChineseModeData(CallbackData, prefix="chinese"):
    pass


class GetDemoData(CallbackData, prefix="demo"):
    lesson_id: int


class PersonalAccountData(CallbackData, prefix="personal_account"):
    pass


class PaginationData(CallbackData, prefix="page"):
    direction: str


class PAPaginationData(CallbackData, prefix="pa_page"):
    direction: str
