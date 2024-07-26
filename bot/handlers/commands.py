
from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram import types
import requests

import config
from messages import templates
from states.auth_states import SignUpStates
from states.password_change_states import PasswordChangeStates

router = Router()


@router.message(CommandStart())
async def start_command_handler(message: types.Message) -> None:
    await message.reply(
        templates.start_message(),
        parse_mode='HTML'
    )


@router.message(Command(commands=['signin']))
async def signin_start(message: types.Message):
    chat_id = message.chat.id
    await message.reply(
        templates.signin_success_message(chat_id, config.AUTH_FORM_URL),
        parse_mode='HTML'
    )


@router.message(Command(commands=['signup']))
async def signup_start(message: types.Message, state: FSMContext):
    await message.reply(
        templates.signup_prompt(),
        parse_mode='HTML'
    )
    await state.set_state(SignUpStates.waiting_for_password)


@router.message(SignUpStates.waiting_for_password)
async def process_signup_password(message: types.Message, state: FSMContext):
    password = message.text
    user_data = {
        'user_id': message.chat.id,
        'username': message.chat.username,
        'password': password,
        'first_name': message.chat.first_name,
        'last_name': message.chat.last_name
    }
    response = requests.post(f'{config.AUTH_API_URL}/signup', json=user_data)
    if response.status_code == 201:
        await message.reply(
            templates.signup_success_message(message.chat.id, config.AUTH_FORM_URL),
            parse_mode='HTML'
        )
    else:
        await message.reply(
            templates.signup_failure_message(),
            parse_mode='HTML'
        )
    await state.clear()


@router.message(Command(commands=['change_password']))
async def change_password_start(message: types.Message, state: FSMContext):
    await message.reply(
        templates.current_password_prompt(),
        parse_mode='HTML'
    )
    await state.set_state(PasswordChangeStates.waiting_for_current_password)


@router.message(PasswordChangeStates.waiting_for_current_password)
async def process_current_password(message: types.Message, state: FSMContext):
    current_password = message.text
    await state.update_data(current_password=current_password)
    await message.reply(
        templates.new_password_prompt(),
        parse_mode='HTML'
    )
    await state.set_state(PasswordChangeStates.waiting_for_new_password)


@router.message(PasswordChangeStates.waiting_for_new_password)
async def process_new_password(message: types.Message, state: FSMContext):
    new_password = message.text
    data = await state.get_data()
    current_password = data['current_password']
    user_id = message.chat.id

    response = requests.patch(
        f'{config.USER_API_URL}/change_password',
        json={'user_id': user_id, 'current_password': current_password, 'new_password': new_password}
    )
    if response.status_code == 200:
        await message.reply(
            templates.password_change_success_message(user_id, config.AUTH_FORM_URL),
            parse_mode='HTML'
        )
    else:
        await message.reply(
            templates.password_change_failure_message(),
            parse_mode='HTML'
        )
    await state.clear()


@router.message(Command(commands=['help']))
async def help_command_handler(message: types.Message) -> None:
    await message.reply(
        templates.help_message(),
        parse_mode='HTML'
    )
