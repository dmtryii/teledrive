
def start_message() -> str:
    return (
        '👋 <b>Welcome!</b> This bot is used for user authorization.\n\n'
        'You can use /signin to sign in or /signup to sign up. Further work will be done on the site.\n\n'
        'This is done to ensure the anonymity of the data and that the files belong only to your account.'
    )


def signin_prompt() -> str:
    return '🔐 <b>Please enter your password:</b>'


def signin_success_message(access_token: str, session_link: str) -> str:
    return (
        f'✅ <b>Successfully signed in!</b>\n\n'
        f'<b>Your access token:</b> <code>{access_token}</code>\n\n'
        f'<b>Session link:</b> <a href="{session_link}">Click here to access your session</a>'
    )


def signin_failure_message() -> str:
    return '❌ <b>Signin failed!</b>'


def signup_prompt() -> str:
    return '🔐 <b>Please enter your password:</b>'


def signup_success_message(access_token: str, session_link: str) -> str:
    return (
        f'✅ <b>Successfully signed up!</b>\n\n'
        f'<b>Your access token:</b> <code>{access_token}</code>\n\n'
        f'<b>Session link:</b> <a href="{session_link}">Click here to access your session</a>'
    )


def signup_failure_message() -> str:
    return '❌ <b>Signup failed!</b>'


def current_password_prompt() -> str:
    return '🔐 <b>Please enter your current password:</b>'


def new_password_prompt() -> str:
    return '🔐 <b>Please enter your new password:</b>'


def password_change_success_message(access_token: str, session_link: str) -> str:
    return (
        f'✅ <b>Password changed successfully!</b>\n\n'
        f'<b>Your new access token:</b> <code>{access_token}</code>\n\n'
        f'<b>Session link:</b> <a href="{session_link}">Click here to access your session</a>'
    )


def password_change_failure_message() -> str:
    return '❌ <b>Password change failed!</b>'


def help_message() -> str:
    return (
        'ℹ️ <b>Commands:</b>\n'
        '/signin - Sign in to your account\n'
        '/signup - Sign up for a new account\n'
        '/change_password - Change your password\n'
        'Follow the prompts after the command.'
    )
