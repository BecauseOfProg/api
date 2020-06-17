from main import app
from core import responses
from core.exceptions import *


@app.errorhandler(400)
def client_error(_):
    response = {
        'code': 0,
        'message': 'Bad request'
    }
    return responses.response(response, 400)


@app.errorhandler(401)
def unauthorized(_):
    response = {
        'code': 0,
        'message': 'Unauthorized'
    }
    return responses.response(response, 401)


@app.errorhandler(403)
def forbidden(_):
    response = {
        'code': 0,
        'message': 'Forbidden'
    }
    return responses.response(response, 403)


@app.errorhandler(404)
def page_not_found(_):
    response = {
        'code': 0,
        'message': 'Not found'
    }
    return responses.response(response, 404)


@app.errorhandler(405)
def method_not_allowed(_):
    response = {
        'code': 0,
        'message': 'Method not allowed'
    }
    return responses.response(response, 405)


@app.errorhandler(PaginationError)
def pagination_error(_):
    response = {
        'code': 0,
        'message': 'Invalid page number. Required type : integer greater than 0'
    }
    return responses.response(response, 400)


@app.errorhandler(InvalidCredentials)
def invalid_credentials(_):
    response = {
        'code': 0,
        'message': 'Invalid email address and/or password'
    }
    return responses.response(response, 400)


@app.errorhandler(DataError)
def data_error(error):
    response = {
        'code': 0,
        'message':
            'Error on the passed data. Try looking at the API documentation for required and optional data : '
            'https://github.com/BecauseOfProg/api-docs',
        'required_data': error.required_data,
        'optional_data': error.optional_data
    }
    return responses.response(response, 400)


@app.errorhandler(NotUnique)
def not_unique(_):
    response = {
        'code': 0,
        'message': 'The resource already exists. Try changing the identifier (URL or username)'
    }
    return responses.response(response, 400)


@app.errorhandler(500)
def internal_server_error(_):
    response = {
        'code': 0,
        'message': 'Internal server error'
    }
    return responses.response(response, 500)
