
from app.exceptions.custom_exception import CustomException


class InvalidUsage(CustomException):
    status_code = 400


class EmptyFieldException(InvalidUsage):
    def __init__(self, message='Field cannot be empty'):
        super().__init__(message)


class PasswordTooShortException(InvalidUsage):
    def __init__(self, message='The password must be longer'):
        super().__init__(message)


class InvalidAgeException(InvalidUsage):
    def __init__(self, message='User must be older'):
        super().__init__(message)


class UsernameAllreadyPresentException(InvalidUsage):
    def __init__(self, message='User with that username is already present'):
        super().__init__(message)
