import time

from werkzeug.exceptions import NotFound
from pony.orm import *
from core.exceptions import DataError

from app.models.users import User
from core.utils import ids, tokens
from core.utils.passwords import ArgonHasher, BcryptHasher


class UsersController:
    @staticmethod
    def fill_informations(user: User):
        fields = ["username", "displayname", "timestamp", "avatar", "description", "biography", "location", "socials", "permissions", "is_email_public"]
        if user.is_email_public:
            fields.append("email")
        return user.to_dict(only=fields)

    @staticmethod
    @db_session
    def get_one(username):
        try:
            return UsersController.fill_informations(User[username])
        except core.ObjectNotFound:
            raise NotFound

    @staticmethod
    @db_session
    def get_one_by_token(token):
        try:
            return UsersController.fill_informations(User.get(token=token))
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
    def update_profile(token, params):
        try:
            user = User.get(token=token)
            user.avatar = params["avatar"]
            user.displayname = params["displayname"]
            user.description = params["description"]
            user.biography = params["biography"]
            user.location = params["location"]
            user.socials = params["socials"]
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
