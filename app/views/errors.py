from pony.orm import *

from main import app
from core import responses
from core.exceptions import *


@app.errorhandler(400)
def client_error(_):
    return responses.fail('badRequest')


@app.errorhandler(401)
def unauthorized(_):
    return responses.fail('unauthorized', code=401)


@app.errorhandler(403)
def forbidden(_):
    return responses.fail('forbidden', code=403)


@app.errorhandler(core.ObjectNotFound)
@app.errorhandler(404)
def page_not_found(_):
    return responses.fail('notFound', code=404)


@app.errorhandler(405)
def method_not_allowed(_):
    return responses.fail('methodNotAllowed', code=405)


@app.errorhandler(PaginationError)
def pagination_error(_):
    return responses.fail('invalidPage')


@app.errorhandler(InvalidCredentials)
def invalid_credentials(_):
    return responses.fail('invalidCredentials')


@app.errorhandler(DataError)
def data_error(error):
    return responses.fail(
        'dataError',
        additional={
            'required_data': error.required_data,
            'optional_data': error.optional_data
        })


@app.errorhandler(NotUnique)
def not_unique(_):
    return responses.fail('alreadyExists')


@app.errorhandler(500)
def internal_server_error(_):
    return responses.fail('internalError', code=500)
