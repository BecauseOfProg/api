from flask import request
from werkzeug.exceptions import NotFound

from app.controllers.users import UsersController
from app.middlewares.body import CheckBody
from app.middlewares.auth import CheckAuth
from app.middlewares.permissions import CheckPermissions
from core import responses
from core.exceptions import DataError
from main import app


@app.route("/api/users", methods=["POST", "GET"])
def all_users():
    if request.method == "GET":
        response = {
            "code": 1,
            "users": UsersController.get_all()
        }
        return responses.response(response)

    elif request.method == "POST":
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
            UsersController.create_one(
                email=request_data["email"], username=request_data["username"], password=request_data["password"])
            return responses.response({"code": 1})
        except DataError:
            return responses.data_error(required_data)


@app.route("/api/users/<string:username>", methods=["GET", "PATCH", "DELETE"])
def one_user(username):
    if request.method == "GET":
        response = {
            "code": 1,
            "user": UsersController.get_one(username)
        }
        return responses.response(response)
    elif request.method == "PATCH":
        required_data = {
            "email": {
                "type": "string",
                "min_length": 6
            },
            "displayname": {
                "type": "string",
                "min_length": 2,
                "max_length": 32
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
            token = request.args.get("token")
            if UsersController.get_one_by_token(token)["username"] != username:
                raise NotFound
            UsersController.update_one(
                token=token, params=request_data)
            return responses.response({"code": 1})
        except DataError:
            return responses.data_error(required_data)
    elif request.method == "DELETE":
        pass


@app.route("/api/users/<string:username>/update-password", methods=["PATCH"])
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


@app.route("/api/users/<string:username>/update-permissions", methods=["PATCH"])
def update_permissions(username):
    pass
