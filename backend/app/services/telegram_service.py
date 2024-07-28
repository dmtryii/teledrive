
import requests

from app.exceptions.telegram_exception import TelegramAPIError, MessageDeletionError
from config import Config


TELEGRAM_BOT_TOKEN = Config.BOT_TOKEN
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}'


def send_document(file, user_id):
    url = f"{TELEGRAM_API_URL}/sendDocument"
    telegram_files = {'document': (file.filename, file)}
    data = {'chat_id': user_id}

    response = requests.post(url, files=telegram_files, data=data)
    if response.status_code != 200:
        raise TelegramAPIError(f"Telegram API error: {response.text}")

    return response.json()


def delete_message(user_id, message_id):
    delete_url = f"{TELEGRAM_API_URL}/deleteMessage"
    delete_data = {'chat_id': user_id, 'message_id': message_id}

    delete_response = requests.post(delete_url, data=delete_data)
    if delete_response.status_code != 200:
        raise MessageDeletionError(f"Failed to delete message: {delete_response.text}")


def get_file_path(file_id):
    url = f"{TELEGRAM_API_URL}/getFile"
    params = {'file_id': file_id}

    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise TelegramAPIError(f"Telegram API error: {response.text}")

    return response.json()['result']['file_path']


def generate_file_url(file_path):
    return f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}"
