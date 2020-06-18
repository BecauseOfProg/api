import time

from werkzeug.exceptions import NotFound
from pony.orm import *

from app.models.users import User
from core.utils import tokens
from core.utils.passwords import ArgonHasher


class UsersController:
    @staticmethod
    def fill_information(user: User, include_permissions: bool = False):
        fields = ['username', 'displayname', 'timestamp', 'picture', 'description', 'biography', 'location', 'socials',
                  'is_email_public']
        if user.is_email_public:
            fields.append('email')
        if include_permissions:
            fields.append('permissions')
        return user.to_dict(only=fields)

    @staticmethod
    @db_session
    def get_all():
        users = list(User.select())
        for user in users:
            users[users.index(user)] = UsersController.fill_information(user)
        return users

    @staticmethod
    @db_session
    def get_one(username):
        user = User[username]
        UsersController.check_active(user)
        return UsersController.fill_information(user)

    @staticmethod
    @db_session
    def get_one_by_token(token):
        user = User.get(token=token)
        if user is None:
            raise NotFound
        UsersController.check_active(user)
        return UsersController.fill_information(user, include_permissions=True)

    @staticmethod
    @db_session
    def get_user_permissions(username):
        user = User[username]
        UsersController.check_active(user)
        return user.permissions

    @staticmethod
    @db_session
    def create_one(email, username, password):
        timestamp = int(time.time())
        token = tokens.generate_token()
        hashed_password = ArgonHasher.generate_password(password)
        user = User(email=email,
                    username=username,
                    displayname=username,
                    password=hashed_password,
                    timestamp=timestamp,
                    token=token
                    )
        commit()
        return True

    @staticmethod
    @db_session
    def update_profile(token, params, optional_data):
        user = User.get(token=token)
        for field in optional_data:
            if field in params:
                setattr(user, field, params[field])
        commit()
        return True

    @staticmethod
    @db_session
    def update_permissions(username, permissions):
        user = User[username]
        user.permissions = permissions
        commit()
        return True

    @staticmethod
    @db_session
    def delete_one(username, admin_token):
        pass

    @staticmethod
    def check_active(user):
        if user.is_activated is False or user.is_verified is False:
            raise NotFound
