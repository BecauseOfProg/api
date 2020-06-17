from main import app
from core.exceptions import PaginationError


@app.errorhandler(400)
def client_error(_):
    response = {
        'code': 0,
        'message': 'Bad request'
    }
    return response, 400, {'Content-Type': 'application/json'}


@app.errorhandler(401)
def unauthorized(_):
    response = {
        'code': 0,
        'message': 'Unauthorized'
    }
    return response, 401, {'Content-Type': 'application/json'}


@app.errorhandler(403)
def forbidden(_):
    response = {
        'code': 0,
        'message': 'Forbidden'
    }
    return response, 403, {'Content-Type': 'application/json'}


@app.errorhandler(404)
def page_not_found(_):
    response = {
        'code': 0,
        'message': 'Not found'
    }
    return response, 404, {'Content-Type': 'application/json'}


@app.errorhandler(405)
def method_not_allowed(_):
    response = {
        'code': 0,
        'message': 'Method not allowed'
    }
    return response, 405, {'Content-Type': 'application/json'}


@app.errorhandler(PaginationError)
def pagination_error(_):
    response = {
        'code': 0,
        'message': 'Invalid page number. Required type : integer greater than 0'
    }
    return response, 400, {'Content-Type': 'application/json'}


@app.errorhandler(500)
def internal_server_error(_):
    response = {
        'code': 0,
        'message': 'Internal server error'
    }
    return response, 500, {'Content-Type': 'application/json'}
