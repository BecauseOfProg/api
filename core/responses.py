import json


def response(data):
    return json.dumps(data), 200, {"Content-Type": "application/json"}


def invalid_username_or_password():
    return json.dumps({
        "code": 0,
        "message": "Invalid email address and/or password"
    }), 400, {"Content-Type": "application/json"}


def data_error(required_data):
    return json.dumps({
        "code": 0,
        "message": "Data error",
        "required_data": required_data
    }), 400, {"Content-Type": "application/json"}
