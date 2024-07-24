
from aiogram.fsm.state import State, StatesGroup


class SignUpStates(StatesGroup):
    waiting_for_password = State()


class SignInStates(StatesGroup):
    waiting_for_password = State()
