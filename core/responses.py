import json


def response(data):
    return json.dumps(data), 200, {'Content-Type': 'application/json'}


def invalid_username_or_password():
    return json.dumps({
        'code': 0,
        'message': 'Invalid email address and/or password'
    }), 400, {'Content-Type': 'application/json'}


def data_error(required_data, optional_data = {}):
    return json.dumps({
        'code': 0,
        'message': 'Data error',
        'required_data': required_data,
        'optional_data': optional_data
    }), 400, {'Content-Type': 'application/json'}


def not_unique():
    return json.dumps({
        'code': 0,
        'message': 'Already exists'
    }), 400, {'Content-Type': 'application/json'}