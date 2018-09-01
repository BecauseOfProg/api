import json

from werkzeug.exceptions import (BadRequest, Forbidden, InternalServerError,
                                 NotFound)

from app.views import errors
from core.config import Config


def response(data):
    return (json.dumps(data), 200, {"Content-Type": "application/json"})


def not_found():
    return errors.page_not_found(NotFound)


def unknown_user():
    response = {
        "code": 0,
        "message": "Unknown user"
    }
    return (json.dumps(response), 404, {"Content-Type": "application/json"})


def forbidden():
    return errors.forbidden(Forbidden)


def invalid_username_or_password():
    response = {
        "code": 0,
        "message": "Invalid email adress and/or password"}
    return (json.dumps(response), 400, {"Content-Type": "application/json"})


def data_error(required_data):
    response = {
        "code": 0,
        "message": "Data error",
        "required_data": required_data
    }
    return (json.dumps(response), 400, {"Content-Type": "application/json"})


def server_error():
    return errors.internal_server_error(InternalServerError)
