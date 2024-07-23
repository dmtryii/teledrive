
from app.exceptions.user_exception import InvalidUsage


class InvalidCredentialsException(InvalidUsage):
    def __init__(self, message='Invalid credentials', status_code=401, payload=None):
        super().__init__(message, status_code, payload)
