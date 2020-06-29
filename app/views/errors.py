from pony.orm import *

from main import app
from core import responses
from core.exceptions import *


@app.errorhandler(400)
def client_error(_):
    return responses.fail('Bad request')


@app.errorhandler(401)
def unauthorized(_):
    return responses.fail('Unauthorized', code=401)


@app.errorhandler(403)
def forbidden(_):
    return responses.fail('Forbidden', code=403)


@app.errorhandler(core.ObjectNotFound)
@app.errorhandler(404)
def page_not_found(_):
    return responses.fail('Not found', code=404)


@app.errorhandler(405)
def method_not_allowed(_):
    return responses.fail('Method not allowed', code=405)


@app.errorhandler(PaginationError)
def pagination_error(_):
    return responses.fail('Invalid page number. Required type : integer greater than 0')


@app.errorhandler(InvalidCredentials)
def invalid_credentials(_):
    return responses.fail('Invalid email address and/or password')


@app.errorhandler(DataError)
def data_error(error):
    return responses.fail(
        'Error on the passed data. Try looking at the API documentation for required and optional data : '
        'https://github.com/BecauseOfProg/api-docs',
        additional={
            'required_data': error.required_data,
            'optional_data': error.optional_data
        })


@app.errorhandler(NotUnique)
def not_unique(_):
    return responses.fail('The resource already exists. Try changing the identifier (URL or username)')


@app.errorhandler(500)
def internal_server_error(_):
    return responses.fail('Internal server error', code=500)
