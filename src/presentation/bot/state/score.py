from aiogram.fsm.state import State, StatesGroup


class Score(StatesGroup):
    subject = State()
    score = State()
