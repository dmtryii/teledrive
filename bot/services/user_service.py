
from aiogram.fsm.context import FSMContext
from aiogram import types
from helpers import fetchers
from states.auth_states import SignUpStates
from states.password_change_states import PasswordChangeStates
import config
from messages import templates


async def handle_start_command(message: types.Message) -> None:
    chat_id = message.chat.id
    is_new_user = not fetchers.get_user_status(chat_id)
    await message.reply(
        templates.start_message(is_new_user=is_new_user),
        parse_mode='HTML'
    )


async def handle_signin_command(message: types.Message) -> None:
    chat_id = message.chat.id
    is_new_user = not fetchers.get_user_status(chat_id)
    if is_new_user:
        await message.reply(
            templates.no_account_message(),
            parse_mode='HTML'
        )
    else:
        await message.reply(
            templates.signin_success_message(chat_id, config.AUTH_FORM_URL),
            parse_mode='HTML'
        )


async def handle_signup_command(message: types.Message, state: FSMContext) -> None:
    chat_id = message.chat.id
    is_new_user = not fetchers.get_user_status(chat_id)
    if not is_new_user:
        await message.reply(
            templates.account_already_message(),
            parse_mode='HTML'
        )
    else:
        await message.reply(
            templates.signup_prompt(),
            parse_mode='HTML'
        )
        await state.set_state(SignUpStates.waiting_for_password)


async def process_signup_password(message: types.Message, state: FSMContext) -> None:
    chat_id = message.chat.id
    password = message.text
    user_data = {
        'user_id': chat_id,
        'username': message.chat.username,
        'password': password,
        'first_name': message.chat.first_name,
        'last_name': message.chat.last_name
    }
    response = fetchers.signup_user(user_data)
    if response and response.status_code == 201:
        await message.reply(
            templates.signup_success_message(chat_id, config.AUTH_FORM_URL),
            parse_mode='HTML'
        )
    else:
        await message.reply(
            templates.signup_failure_message(),
            parse_mode='HTML'
        )
    await state.clear()


async def handle_change_password_command(message: types.Message, state: FSMContext) -> None:
    chat_id = message.chat.id
    is_new_user = not fetchers.get_user_status(chat_id)
    if is_new_user:
        await message.reply(
            templates.no_account_message(),
            parse_mode='HTML'
        )
    else:
        await message.reply(
            templates.current_password_prompt(),
            parse_mode='HTML'
        )
        await state.set_state(PasswordChangeStates.waiting_for_current_password)


async def process_current_password(message: types.Message, state: FSMContext) -> None:
    current_password = message.text
    await state.update_data(current_password=current_password)
    await message.reply(
        templates.new_password_prompt(),
        parse_mode='HTML'
    )
    await state.set_state(PasswordChangeStates.waiting_for_new_password)


async def process_new_password(message: types.Message, state: FSMContext) -> None:
    new_password = message.text
    data = await state.get_data()
    current_password = data['current_password']
    user_id = message.chat.id

    response = fetchers.change_password(user_id, current_password, new_password)
    if response and response.status_code == 200:
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


async def handle_help_command(message: types.Message) -> None:
    chat_id = message.chat.id
    is_new_user = not fetchers.get_user_status(chat_id)
    await message.reply(
        templates.help_message(is_new_user=is_new_user),
        parse_mode='HTML'
    )
