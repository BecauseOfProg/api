from pony.orm import *

from main import app
from core import responses
from core.exceptions import *


@app.errorhandler(400)
def client_error(_):
    return responses.response({
        'code': 0,
        'message': 'Bad request'
    }, 400)


@app.errorhandler(401)
def unauthorized(_):
    return responses.response({
        'code': 0,
        'message': 'Unauthorized'
    }, 401)


@app.errorhandler(403)
def forbidden(_):
    return responses.response({
        'code': 0,
        'message': 'Forbidden'
    }, 403)


@app.errorhandler(core.ObjectNotFound)
@app.errorhandler(404)
def page_not_found(_):
    return responses.response({
        'code': 0,
        'message': 'Not found'
    }, 404)


@app.errorhandler(405)
def method_not_allowed(_):
    return responses.response({
        'code': 0,
        'message': 'Method not allowed'
    }, 405)


@app.errorhandler(PaginationError)
def pagination_error(_):
    return responses.response({
        'code': 0,
        'message': 'Invalid page number. Required type : integer greater than 0'
    }, 400)


@app.errorhandler(InvalidCredentials)
def invalid_credentials(_):
    return responses.response({
        'code': 0,
        'message': 'Invalid email address and/or password'
    }, 400)


@app.errorhandler(DataError)
def data_error(error):
    return responses.response({
        'code': 0,
        'message':
            'Error on the passed data. Try looking at the API documentation for required and optional data : '
            'https://github.com/BecauseOfProg/api-docs',
        'required_data': error.required_data,
        'optional_data': error.optional_data
    }, 400)


@app.errorhandler(NotUnique)
def not_unique(_):
    return responses.response({
        'code': 0,
        'message': 'The resource already exists. Try changing the identifier (URL or username)'
    }, 400)


@app.errorhandler(500)
def internal_server_error(_):
    return responses.response({
        'code': 0,
        'message': 'Internal server error'
    }, 500)
