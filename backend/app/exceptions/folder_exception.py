from app.exceptions.user_exception import InvalidUsage


class FolderException(InvalidUsage):
    def __init__(self, message, status_code=400):
        super().__init__(message, status_code)
