from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    help = State()
    lessons = State()
