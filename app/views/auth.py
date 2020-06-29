from flask import request

from app.controllers.users import UsersController
from app.controllers.auth import AuthController
from app.middlewares.auth import CheckAuth
from app.middlewares.body import CheckBody
from core import responses
from main import app


@app.route('/v1/auth', methods=['POST'])
def create_session():
    required_data = {
        'email': {
            'type': 'string'
        },
        'password': {
            'type': 'string'
        }
    }
    data = CheckBody.call(request, required_data=required_data)
    user, token = AuthController.create_session(data['email'], data['password'])
    return responses.success({
        'user': user,
        'token': token
    })


@app.route('/v1/auth/data', methods=['GET'])
def get_information():
    CheckAuth(request)
    return responses.success(UsersController.get_one_by_token(request.headers.get('Authorization')))
