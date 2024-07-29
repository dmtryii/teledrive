from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram import types

from services import user_service
from states.auth_states import SignUpStates
from states.password_change_states import PasswordChangeStates

router = Router()


@router.message(CommandStart())
async def start_command_handler(message: types.Message) -> None:
    await user_service.handle_start_command(message)


@router.message(Command(commands=['signin']))
async def signin_start(message: types.Message) -> None:
    await user_service.handle_signin_command(message)


@router.message(Command(commands=['signup']))
async def signup_start(message: types.Message, state: FSMContext) -> None:
    await user_service.handle_signup_command(message, state)


@router.message(SignUpStates.waiting_for_password)
async def process_signup_password(message: types.Message, state: FSMContext) -> None:
    await user_service.process_signup_password(message, state)


@router.message(Command(commands=['change_password']))
async def change_password_start(message: types.Message, state: FSMContext) -> None:
    await user_service.handle_change_password_command(message, state)


@router.message(PasswordChangeStates.waiting_for_current_password)
async def process_current_password(message: types.Message, state: FSMContext) -> None:
    await user_service.process_current_password(message, state)


@router.message(PasswordChangeStates.waiting_for_new_password)
async def process_new_password(message: types.Message, state: FSMContext) -> None:
    await user_service.process_new_password(message, state)


@router.message(Command(commands=['help']))
async def help_command_handler(message: types.Message) -> None:
    await user_service.handle_help_command(message)
