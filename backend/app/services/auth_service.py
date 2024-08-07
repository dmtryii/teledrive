
from flask_jwt_extended import create_access_token

from app.exceptions.auth_exception import InvalidCredentialsException
from app.extensions import db
from app.exceptions.user_exception import (
    EmptyFieldException,
    PasswordTooShortException, 
    UsernameAllreadyPresentException)
from app.models.users import BaseUser, Role

from app.services import folder_services


def signin(user_id: int, password: str) -> str:
    if not user_id:
        raise EmptyFieldException(message='Missing user_id')
    
    if not password:
        raise EmptyFieldException(message='Missing password')
    
    user = BaseUser.query.filter_by(id=user_id).first()
    if not user or not user.check_password(password):
        raise InvalidCredentialsException()

    return create_access_token(identity=user.id)


def signup(user_id: int, username: str, password: str, first_name: str, last_name: str) -> str:
       
    if len(password) < 6:
        raise PasswordTooShortException(message='Password must be at least 6 characters long')
    
    user = BaseUser.query.filter_by(id=user_id).first()
    
    if user:
        raise UsernameAllreadyPresentException()
        
    new_user = BaseUser(
        id=user_id,
        username=username,
        first_name=first_name,
        last_name=last_name
    )
    
    __set_default_role(new_user)
    
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    folder_services.get_root_folder(user_id)

    return create_access_token(identity=new_user.id)


def __set_default_role(user: BaseUser) -> None:
    role = Role.query.filter_by(name='default').first()

    if not role:
        role = Role(name='default')
        
    user.roles.append(role)
