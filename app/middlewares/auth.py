from werkzeug.exceptions import Unauthorized

from app.controllers.users import UsersController


class CheckAuth:
    def __init__(self, request):
        try:
            token = request.args.get("token")
            if token is None:
                raise Unauthorized
            if UsersController.get_one_by_token(token) == False:
                raise Unauthorized
        except KeyError:
            raise Unauthorized
