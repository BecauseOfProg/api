from flask import request
from werkzeug.exceptions import NotFound

from app.controllers.auth import AuthController
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
        CheckBody(request, required_data=required_data)
        request_data = request.json
        data = AuthController.create_session(email=request_data['email'], password=request_data['password'])
        response = {
            'code': 1,
            'data': data
        }
        return responses.response(response)
    except DataError:
        return responses.data_error(required_data)
    except InvalidCreds:
        return responses.invalid_username_or_password()
