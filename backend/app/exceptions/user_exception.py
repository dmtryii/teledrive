
class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class EmptyFieldException(InvalidUsage):
    def __init__(self, message='Field cannot be empty', status_code=None, payload=None):
        super().__init__(message, status_code, payload)


class PasswordTooShortException(InvalidUsage):
    def __init__(self, message='The password must be longer', status_code=None, payload=None):
        super().__init__(message, status_code, payload)


class InvalidAgeException(InvalidUsage):
    def __init__(self, message='User must be older', status_code=None, payload=None):
        super().__init__(message, status_code, payload)


class UsernameAllreadyPresentException(InvalidUsage):
    def __init__(self, message='User with that username is already present', status_code=None, payload=None):
        super().__init__(message, status_code, payload)
        
        
class InvalidEmailException(InvalidUsage):
    def __init__(self, message='Invalid email address', status_code=None, payload=None):
        super().__init__(message, status_code, payload)


class IncorrectPasswordException(Exception):
    def __init__(self, message='Incorrect current password', status_code=403, payload=None):
        super().__init__(message, status_code, payload)
