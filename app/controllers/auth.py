from pony.orm import db_session
from app.models.users import User
from app.controllers.users import UsersController
from core.exceptions import InvalidCredentials
from core.utils.passwords import ArgonHasher, BcryptHasher


class AuthController:
    @staticmethod
    @db_session
    def create_session(email: str, password: str):
        user = User.get(email=email)
        if user is None:
            raise InvalidCredentials
        
        if user.password_type == 'bcrypt':
            if BcryptHasher.are_password_same(user.password, password):
                return UsersController.get_one_by_token(user.token), user.token
            else:
                raise InvalidCredentials
        else:
            if ArgonHasher.are_password_same(user.password, password):
                return UsersController.get_one_by_token(user.token), user.token
            else:
                raise InvalidCredentials
