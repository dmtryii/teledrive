
from aiogram.fsm.state import State, StatesGroup


class PasswordChangeStates(StatesGroup):
    waiting_for_current_password = State()
    waiting_for_new_password = State()
