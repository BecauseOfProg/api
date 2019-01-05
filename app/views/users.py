from flask import request
from werkzeug.exceptions import NotFound
from mongoengine.errors import NotUniqueError

from app.controllers.users import UsersController
from app.middlewares.body import CheckBody
from app.middlewares.auth import CheckAuth
from app.middlewares.permissions import CheckPermissions
from core import responses
from core.exceptions import DataError
from main import app


@app.route("/v1/users", methods=["POST"])
def get_all_users():
    required_data = {
        "email": {
            "type": "string",
            "min_length": 6
        },
        "username": {
            "type": "string",
            "min_length": 2,
            "max_length": 32
        },
        "password": {
            "type": "string",
            "min_length": 8
        }
    }
    try:
        CheckBody(request, required_data=required_data)
        request_data = request.json
        UsersController.create_one(email=request_data["email"],
                                   username=request_data["username"],
                                   password=request_data["password"])
        return responses.response({"code": 1})
    # except NotUniqueError:
    #     return responses.not_unique()
    except DataError:
        return responses.data_error(required_data)


@app.route("/v1/users/<string:username>", methods=["GET"])
def get_one_user(username):
    response = {
        "code": 1,
        "user": UsersController.get_one(username)
    }
    return responses.response(response)


@app.route("/v1/users/<string:username>", methods=["PATCH"])
def update_profile(username):
    required_data = {
        "displayname": {
            "type": "string",
            "min_length": 2,
            "max_length": 32
        },
        "picture": {
            "type": "string"
        },
        "description": {
            "type": "string"
        },
        "biography": {
            "type": "string"
        },
        "location": {
            "type": "string",
        },
        "socials": {
            "type": "list of dicts"
        }
    }
    try:
        CheckBody(request, required_data)
        CheckAuth(request)
        request_data = request.json
        token = request.headers.get("Authorization")
        if UsersController.get_one_by_token(token)["username"] != username:
            raise NotFound
        UsersController.update_profile(token=token,
                                   params=request_data)
        return responses.response({"code": 1})
    except DataError:
        return responses.data_error(required_data)


@app.route("/v1/users/<string:username>/email", methods=["PATCH"])
def update_email(username):
    required_data = {
        "new_email": {
            "type": "string",
            "min_length": 6
        }
    }

@app.route("/v1/users/<string:username>/password", methods=["PATCH"])
def update_password(username):
    required_data = {
        "old_password": {
            "type": "string",
            "min_length": 8
        },
        "new_password": {
            "type": "string",
            "min_length": 8
        }
    }


@app.route("/v1/users/<string:username>/permissions", methods=["PATCH"])
def update_permissions(username):
    required_data = {
        "permissions": {
            "type": "list"
        }
    }
    try:
        CheckPermissions(request, permissions=["USER_WRITE"])
        request_data = request.json
        print(request_data)
        UsersController.update_permissions(username, request_data["permissions"])
        return responses.response({"code": 1})
    except DataError:
        return responses.data_error(required_data)

