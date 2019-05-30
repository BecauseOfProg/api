from flask import request
from werkzeug.exceptions import NotFound

from app.controllers.users import UsersController
from app.middlewares.body import CheckBody
from app.middlewares.auth import CheckAuth
from app.middlewares.permissions import CheckPermissions
from core import responses
from core.exceptions import DataError
from main import app

@app.route('/v1/users', methods=['GET'])
def get_all_users():
    CheckPermissions(request, permissions=['USER_WRITE'])
    response = {
        'code': 1,
        'data': UsersController.get_all()
    }
    return responses.response(response)

@app.route('/v1/users/<string:username>', methods=['GET'])
def get_one_user(username):
    response = {
        'code': 1,
        'user': UsersController.get_one(username)
    }
    return responses.response(response)

@app.route('/v1/users/<string:username>/permissions', methods=['GET'])
def get_user_permissions(username):
    CheckPermissions(request, permissions=['USER_WRITE'])
    response = {
        'code': 1,
        'permissions': UsersController.get_user_permissions(username)
    }
    return responses.response(response)

@app.route('/v1/users', methods=['POST'])
def create_user():
    required_data = {
        'email': {
            'type': 'string',
            'min_length': 6
        },
        'username': {
            'type': 'string',
            'min_length': 2,
            'max_length': 32
        },
        'password': {
            'type': 'string',
            'min_length': 8
        }
    }
    try:
        data = CheckBody.call(request, required_data=required_data, optional_data={})
        UsersController.create_one(email=data['email'],
                                   username=data['username'],
                                   password=data['password'])
        return responses.response({'code': 1})
    except DataError:
        return responses.data_error(required_data)

@app.route('/v1/users/<string:username>', methods=['PATCH'])
def update_profile(username):
    optional_data = {
        'displayname': {
            'type': 'string',
            'min_length': 2,
            'max_length': 32
        },
        'picture': {
            'type': 'string'
        },
        'description': {
            'type': 'string'
        },
        'biography': {
            'type': 'string'
        },
        'location': {
            'type': 'string',
        },
        'socials': {
            'type': 'list<dict>'
        }
    }
    data = CheckBody.call(request, required_data={}, optional_data=optional_data)
    CheckAuth(request)
    token = request.headers.get('Authorization')
    if UsersController.get_one_by_token(token)['username'] != username:
        raise NotFound
    UsersController.update_profile(token=token,
                                   params=data['optional'],
                                   optional_data=optional_data)
    return responses.response({'code': 1})

@app.route('/v1/users/<string:username>/email', methods=['PATCH'])
def update_email(username):
    required_data = {
        'new_email': {
            'type': 'string',
            'min_length': 6
        }
    }

@app.route('/v1/users/<string:username>/password', methods=['PATCH'])
def update_password(username):
    required_data = {
        'old_password': {
            'type': 'string',
            'min_length': 8
        },
        'new_password': {
            'type': 'string',
            'min_length': 8
        }
    }

@app.route('/v1/users/<string:username>/permissions', methods=['PATCH'])
def update_permissions(username):
    required_data = {
        'permissions': {
            'type': 'list'
        }
    }
    try:
        CheckPermissions(request, permissions=['USER_WRITE'])
        request_data = request.json
        UsersController.update_permissions(username, request_data['permissions'])
        return responses.response({'code': 1})
    except DataError:
        return responses.data_error(required_data)

