from app import CustomException
from app.exceptions.user_exception import InvalidUsage


class FileUploadError(InvalidUsage):
    def __init__(self, message, status_code=400):
        super().__init__(message, status_code)


class DeletionError(CustomException):
    def __init__(self, message, status_code=500):
        super().__init__(message, status_code)


class FileNotFoundException(CustomException):
    def __init__(self, message, status_code=404):
        super().__init__(message, status_code)
