from werkzeug.exceptions import Unauthorized, NotFound

from app.controllers.users import UsersController


class CheckAuth:
    @staticmethod
    def call(request):
        try:
            token = request.headers.get('Authorization')
            if token is None:
                raise Unauthorized
            user = UsersController.get_one_by_token(token)
        except NotFound:
            raise Unauthorized
        except KeyError:
            raise Unauthorized
