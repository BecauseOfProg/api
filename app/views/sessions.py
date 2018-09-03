from flask import request
from werkzeug.exceptions import NotFound

from app.controllers.sessions import SessionsController
from app.middlewares.body import CheckBody
from core import responses
from core.exceptions import InvalidCreds, DataError
from main import app


@app.route('/v1/sessions', methods=["POST"])
def create_session():
    if request.get_json == {}:
        raise NotFound
    else:
        required_data = {
            "email": {
                "type": "string"
            },
            "password": {
                "type": "string"
            }
        }
        try:
            CheckBody(request, required_data=required_data)
            request_data = request.json
            token = SessionsController.create_session(
                request_data["email"], request_data["password"])
            response = {
                "token": token
            }
            return responses.response(response)
        except DataError:
            return responses.data_error(required_data)
        except InvalidCreds:
            return responses.invalid_username_or_password()
