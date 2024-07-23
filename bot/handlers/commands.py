
from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram import types
import requests

import config
from states.auth_states import AuthStates
from states.password_change_states import PasswordChangeStates

router = Router()


@router.message(Command(commands=['signin']))
async def signin_start(message: types.Message, state: FSMContext):
    await message.reply('Please enter your password:')
    await state.set_state(AuthStates.waiting_for_password)


@router.message(AuthStates.waiting_for_password)
async def process_signin_password(message: types.Message, state: FSMContext):
    password = message.text
    user_id = message.chat.id
    response = requests.post(f'{config.AUTH_API_URL}/signin', json={'user_id': user_id, 'password': password})
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        await message.reply(f'Successfully signed in! Your access token: {access_token}')
    else:
        await message.reply('Signin failed!')
    await state.clear()


@router.message(Command(commands=['signup']))
async def signup_start(message: types.Message, state: FSMContext):
    await message.reply('Please enter your password:')
    await state.set_state(AuthStates.waiting_for_password)


@router.message(AuthStates.waiting_for_password)
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
        access_token = response.json().get('access_token')
        await message.reply(f'Successfully signed up! Your access token: {access_token}')
    else:
        await message.reply('Signup failed!')
    await state.clear()


@router.message(Command(commands=['change_password']))
async def change_password_start(message: types.Message, state: FSMContext):
    await message.reply('Please enter your current password:')
    await state.set_state(PasswordChangeStates.waiting_for_current_password)


@router.message(PasswordChangeStates.waiting_for_current_password)
async def process_current_password(message: types.Message, state: FSMContext):
    current_password = message.text
    await state.update_data(current_password=current_password)
    await message.reply('Please enter your new password:')
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
        access_token = response.json().get('access_token')
        await message.reply(f'Password changed successfully! Your new access token: {access_token}')
    else:
        await message.reply('Password change failed!')
    await state.clear()


@router.message(CommandStart())
async def start_command_handler(message: types.Message) -> None:
    await message.reply('Hi, you can use /signin to sign in or /signup to sign up.')


@router.message(Command(commands=['help']))
async def help_command_handler(message: types.Message) -> None:
    await message.reply('Use /signin to sign in and /signup to sign up. Follow the prompts after the command.')
