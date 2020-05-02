from flask import request
from werkzeug.exceptions import Unauthorized

from app.controllers.arduino import ArduinoController
from app.controllers.users import UsersController
from app.middlewares.body import CheckBody
from app.middlewares.auth import CheckAuth
from app.middlewares.permissions import CheckPermissions
from core import responses
from core.exceptions import DataError
from main import app


@app.route('/v1/arduino-projects', methods=['GET'])
def get_all_projects():
    response = {
        'code': 1,
        'data': ArduinoController.get_all()
    }
    return responses.response(response)

@app.route('/v1/arduino-projects/staff', methods=['GET'])
def get_projects_from_staff():
    response = {
        'code': 1,
        'data': ArduinoController.get_from_staff()
    }
    return responses.response(response)

@app.route('/v1/arduino-projects/featured', methods=['GET'])
def get_featured_projects():
    response = {
        'code': 1,
        'data': ArduinoController.get_featured()
    }
    return responses.response(response)

@app.route('/v1/arduino-projects/last', methods=['GET'])
def get_last_project():
    response = {
        'code': 1,
        'data': ArduinoController.get_last()
    }
    return responses.response(response)


@app.route('/v1/arduino-projects', methods=['POST'])
def create_project():
    required_data = {
        'url': {
            'type': 'string',
            'min_length': 5,
            'max_length': 64
        },
        'name': {
            'type': 'string',
            'min_length': 5,
            'max_length': 64
        },
        'summary': {
            'type': 'string',
            'min_length': 10,
            'max_length': 250
        }
    }
    optional_data = {
        'illustration': {
            'type': 'string'
        },
        'video': {
            'type': 'string'
        },
        'link': {
            'type': 'string'
        },
        'description': {
            'type': 'string',
            'min_length': 25
        }
    }
    try:
        data = CheckBody.call(request, required_data=required_data, optional_data=optional_data)
        CheckAuth(request)
        author = UsersController.get_one_by_token(request.headers.get('Authorization'))
        data['author_username'] = author['username']
        if 'ARDUINO_STAFF' in author['permissions']:
            data['from_staff'] = True
        else:
            data['from_staff'] = False
        ArduinoController.create_one(params=data,
                                     optional_data=optional_data
                                     )
        return responses.response({'code': 1}, 201)
    except DataError:
        return responses.data_error(required_data, optional_data)


@app.route('/v1/arduino-projects/<string:url>', methods=['GET'])
def one_project(url):
    response = {
        'code': 1,
        'data': ArduinoController.get_one(url)
    }
    return responses.response(response)

@app.route('/v1/arduino-projects/<string:url>', methods=['PATCH'])
def edit_project(url):
    optional_data = {
        'name': {
            'type': 'string',
            'min_length': 5,
            'max_length': 64
        },
        'summary': {
            'type': 'string',
            'min_length': 10,
            'max_length': 250
        },
        'illustration': {
            'type': 'string'
        },
        'video': {
            'type': 'string'
        },
        'link': {
            'type': 'string'
        },
        'description': {
            'type': 'string',
            'min_length': 25
        }
    }
    try:
        project = ArduinoController.get_one(url)
        data = CheckBody.call(request, required_data={}, optional_data=optional_data)
        CheckAuth(request)
        token = request.headers.get('Authorization')
        if UsersController.get_one_by_token(token)['username'] != project['author']['username']:
            raise Unauthorized
        ArduinoController.update_one(url=url,
                                     params=data['optional'],
                                     optional_data=optional_data)
        return responses.no_content()
    except DataError:
        return responses.data_error({}, optional_data)

@app.route('/v1/arduino-projects/<string:url>', methods=['DELETE'])
def delete_project(url):
    project = ArduinoController.get_one(url)
    CheckAuth(request)
    token = request.headers.get('Authorization')
    if UsersController.get_one_by_token(token)['username'] != project['author']['username']:
        raise Unauthorized
    ArduinoController.delete_one(url)
    return responses.no_content()
