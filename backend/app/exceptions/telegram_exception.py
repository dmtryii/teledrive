
from app.exceptions.custom_exception import CustomException
from app.exceptions.user_exception import InvalidUsage


class TelegramAPIError(CustomException):
    def __init__(self, message, status_code=500):
        super().__init__(message, status_code)


class MessageDeletionError(CustomException):
    def __init__(self, message, status_code=500):
        super().__init__(message, status_code)


class TelegramFileNotFoundError(InvalidUsage):
    def __init__(self, message, status_code=404):
        super().__init__(message, status_code)
