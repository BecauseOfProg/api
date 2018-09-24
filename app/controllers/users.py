import time

from werkzeug.exceptions import NotFound
from mongoengine.errors import ValidationError
from core.exceptions import DataError

from app.models.users import User
from core.utils import ids, passwords, tokens


class UsersController:
    @staticmethod
    def fill_informations(user):
        response = {
            "user_id": user.user_id,
            "timestamp": user.timestamp,
            "username": user.username,
            "displayname": user.displayname,
            "avatar": user.avatar,
            "description": user.description,
            "biography": user.biography,
            "location": user.location,
            "socials": user.socials,
            "permissions": user.permissions,
            "is_email_public": user.is_email_public
        }
        if user.is_email_public:
            response.update({"email": user.email})
        return response

    @staticmethod
    def get_one(username):
        users = {}
        for user in User.objects(username=username, is_activated=True):
            users = UsersController.fill_informations(user)
        if users == {}:
            raise NotFound
        else:
            return users

    @staticmethod
    def get_one_by_token(token):
        users = {}
        for user in User.objects(token=token):
            users = UsersController.fill_informations(user)
        if users == {}:
            raise NotFound
        else:
            return users

    @staticmethod
    def create_one(email, username, password):
        try:
            timestamp = int(time.time())
            token = tokens.generate_token()
            user_id = ids.generate_id()
            hashed_password = passwords.generate_password(password)
            user = User(email=email,
                        username=username,
                        displayname=username,
                        password=hashed_password,
                        timestamp=timestamp,
                        token=token,
                        user_id=user_id)
            user.save()
            return True
        except ValidationError:
            raise DataError

    @staticmethod
    def update_one(token, params):
        try:
            User.objects(token=token).update_one(set__email=params["email"],
                                                 set__displayname=params["displayname"],
                                                 set__description=params["description"],
                                                 set__biography=params["biography"],
                                                 set__location=params["location"],
                                                 set__socials=params["socials"])
        except ValidationError:
            raise DataError

    @staticmethod
    def delete_one(username, admin_token):
        pass
