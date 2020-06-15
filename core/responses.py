def response(data, code=200):
    return data, code, {'Content-Type': 'application/json'}


def no_content():
    return response('', 204)


def invalid_username_or_password():
    response = {
        'code': 0,
        'message': 'Invalid email address and/or password'
    }
    return response, 400, {'Content-Type': 'application/json'}


def data_error(required_data, optional_data=None):
    if optional_data is None:
        optional_data = {}

    response = {
        'code': 0,
        'message':
            'Error on the passed data. Try looking at the API documentation for required and optional data : '
            'https://github.com/BecauseOfProg/api-docs',
        'required_data': required_data,
        'optional_data': optional_data
    }
    return response, 400, {'Content-Type': 'application/json'}


def not_unique():
    response = {
        'code': 0,
        'message': 'The resource already exists. Try changing the identifier (URL or username)'
    }
    return response, 400, {'Content-Type': 'application/json'}
