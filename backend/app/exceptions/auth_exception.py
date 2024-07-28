
from app.exceptions.user_exception import InvalidUsage


class InvalidCredentialsException(InvalidUsage):
    def __init__(self, message='Invalid credentials', status_code=401):
        super().__init__(message, status_code)


class UnauthorizedError(InvalidUsage):
    def __init__(self, message, status_code=403):
        super().__init__(message, status_code)


class IncorrectPasswordException(InvalidUsage):
    def __init__(self, message='Incorrect current password', status_code=403):
        super().__init__(message, status_code)
