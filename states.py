from aiogram.fsm.state import State, StatesGroup


class Users(StatesGroup):
    choice_day=State()
    choice_time=State()
    choice_service=State()
