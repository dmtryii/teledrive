
def start_message() -> str:
    return (
        '👋 <b>Welcome!</b> This bot is used for user authorization.\n\n'
        'You can use <b>/signin</b> to sign in or <b>/signup</b> to sign up. Further work will be done on the site.\n\n'
        'This is done to ensure the anonymity of the data and that the files belong only to your account.\n\n'
        'For a list of commands and their usage, type <b>/help</b>. If you need assistance at any time, this command will guide you.'
    )


def signin_success_message(user_id: int, session_link: str) -> str:
    return (
        f'🔗 <b>Session link:</b> <a href="{session_link}?user_id={user_id}">Click here to access your session</a>'
    )


def signup_prompt() -> str:
    return '🔐 <b>Please enter your password:</b>'


def signup_success_message(user_id: int, session_link: str) -> str:
    return (
        f'✅ <b>Successfully signed up!</b>\n\n'
        f'🔗 <b>Session link:</b> <a href="{session_link}?user_id={user_id}">Click here to access your session</a>'
    )


def signup_failure_message() -> str:
    return '❌ <b>Signup failed!</b>'


def current_password_prompt() -> str:
    return '🔐 <b>Please enter your current password:</b>'


def new_password_prompt() -> str:
    return '🔐 <b>Please enter your new password:</b>'


def password_change_success_message(user_id: int, session_link: str) -> str:
    return (
        f'✅ <b>Password changed successfully!</b>\n\n'
        f'🔗 <b>Session link:</b> <a href="{session_link}?user_id={user_id}">Click here to access your session</a>'
    )


def password_change_failure_message() -> str:
    return '❌ <b>Password change failed!</b>'


def help_message() -> str:
    return (
        'ℹ️ <b>Commands:</b>\n'
        '🔑 <b>/signin</b> - Sign in to your account\n'
        '📝 <b>/signup</b> - Sign up for a new account\n'
        '🔄 <b>/change_password</b> - Change your password\n'
        'Follow the prompts after the command.'
    )
