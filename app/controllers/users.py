import time

from werkzeug.exceptions import NotFound
from pony.orm import *

from app.models.users import User
from core.utils import tokens
from core.utils.passwords import ArgonHasher


class UsersController:
    @staticmethod
    def fill_information(user: User, additional_fields=None):
        if additional_fields is None:
            additional_fields = []

        fields = ['username', 'displayname', 'timestamp', 'picture', 'description', 'biography', 'location', 'socials',
                  'is_email_public'] + additional_fields
        if user.is_email_public:
            fields.append('email')
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
        try:
            user = User[username]
            if user.is_activated is False or user.is_verified is False:
                raise NotFound
            return UsersController.fill_information(user)
        except core.ObjectNotFound:
            raise NotFound

    @staticmethod
    @db_session
    def get_one_by_token(token):
        try:
            user = User.get(token=token)
            if user is None:
                raise NotFound
            if user.is_activated is False or user.is_verified is False:
                raise NotFound
            return UsersController.fill_information(user, additional_fields=['permissions'])
        except core.ObjectNotFound:
            raise NotFound

    @staticmethod
    @db_session
    def get_user_permissions(username):
        try:
            user = User[username]
            if user.is_activated is False or user.is_verified is False:
                raise NotFound
            return user.permissions
        except core.ObjectNotFound:
            raise NotFound

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
        try:
            user = User.get(token=token)
            for field in optional_data:
                if field in params:
                    setattr(user, field, params[field])
            commit()
            return True
        except core.ObjectNotFound:
            raise NotFound

    @staticmethod
    @db_session
    def update_permissions(username, permissions):
        try:
            user = User[username]
            user.permissions = permissions
            commit()
            return True
        except core.ObjectNotFound:
            raise NotFound

    @staticmethod
    @db_session
    def delete_one(username, admin_token):
        pass
