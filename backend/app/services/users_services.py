
from typing import List

from flask_jwt_extended import create_access_token

from app.extensions import db
from app.exceptions.auth_exception import InvalidCredentialsException, IncorrectPasswordException
from app.models.users import BaseUser
from app.exceptions.user_exception import PasswordTooShortException


def get_all() -> List[BaseUser]:
    return BaseUser.query.all()


def get_by_id(user_id: int) -> BaseUser:
    user = BaseUser.query.filter_by(id=user_id).first()

    if not user:
        raise InvalidCredentialsException(message='User not found')

    return user


def change_password(user_id: int, current_password: str, new_password: str) -> str:
    if len(new_password) < 6:
        raise PasswordTooShortException(message='Password must be at least 6 characters long')

    user = BaseUser.query.filter_by(id=user_id).first()

    if not user:
        raise InvalidCredentialsException(message='User not found')

    if not user.check_password(current_password):
        raise IncorrectPasswordException()

    user.set_password(new_password)

    db.session.commit()

    return create_access_token(identity=user.id)
