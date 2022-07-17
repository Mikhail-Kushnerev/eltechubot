from aiogram.dispatcher.filters.state import StatesGroup, State


class Test(StatesGroup):
    step_one = State()
    step_two = State()
    step_three = State()
