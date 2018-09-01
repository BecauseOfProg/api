from app.models.users import User
from core.exceptions import InvalidCreds
from core.utils import passwords


class SessionsController:
    @staticmethod
    def create_session(email, password):
        for user in User.objects(email=email):
            if passwords.are_password_same(user.password, password):
                return user.token
            else:
                raise InvalidCreds

        raise InvalidCreds
