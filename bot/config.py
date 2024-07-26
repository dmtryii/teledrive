import os

from dotenv import load_dotenv

load_dotenv()

AUTH_FORM_URL = os.getenv('AUTH_FORM_URL')

BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_WEBHOOK_URL = os.getenv('BOT_WEBHOOK_URL')
BOT_WEBHOOK_PATH = os.getenv('BOT_WEBHOOK_PATH')
BOT_WEBHOOK_PORT = os.getenv('BOT_WEBHOOK_PORT')

AUTH_API_URL = os.getenv('AUTH_API_URL')
USER_API_URL = os.getenv('USER_API_URL')
