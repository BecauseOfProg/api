from flask import request
from werkzeug.exceptions import NotFound

from app.controllers.users import UsersController
from app.controllers.auth import AuthController
from app.middlewares.auth import CheckAuth
from app.middlewares.body import CheckBody
from core import responses
from core.exceptions import InvalidCreds, DataError
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
    try:
        data = CheckBody.call(request, required_data=required_data, optional_data={})
        user_data = AuthController.create_session(email=data['email'], password=data['password'])
        response = {
            'code': 1,
            'data': user_data
        }
        return responses.response(response)
    except DataError:
        return responses.data_error(required_data)
    except InvalidCreds:
        return responses.invalid_username_or_password()


@app.route('/v1/auth/data', methods=['GET'])
def get_information():
    CheckAuth(request)
    return responses.response({
        'code': 1,
        'data': UsersController.get_one_by_token(request.headers.get('Authorization'))
    })
