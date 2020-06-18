from werkzeug.exceptions import Forbidden

from app.controllers.users import UsersController

from .auth import CheckAuth


class CheckPermissions:
    def __init__(self, request, permissions):
        CheckAuth(request)
        user = UsersController.get_one_by_token(request.headers.get('Authorization'))
        for permission in permissions:
            if permission not in user['permissions']:
                raise Forbidden
