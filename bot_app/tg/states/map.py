from aiogram.fsm.state import State, StatesGroup


class MapState(StatesGroup):
    map = State()
    tag_map = State()
    report = State()
    summary = State()
    total_summary = State()
