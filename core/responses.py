ERRORS = {
    'badRequest': "You performed a bad request.",
    'unauthorized': 'You must be authenticated in order to perform this action.',
    'forbidden': "You don't have the required permission to perform this action.",
    'notFound': "The item or endpoint wasn't found. Try making a different query.",
    'methodNotAllowed': "The method you used isn't allowed for this endpoint.",
    'invalidPage': 'Invalid page number. Required type : integer greater than 0',
    'invalidCredentials': 'Invalid email address and/or password',
    'dataError': 'Error on the passed data.',
    'alreadyExists': 'The resource already exists. Try changing the identifier',
    'internalError': 'Internal server error'
}


def response(data: dict, code: int):
    return data, code


def success(data: dict, additional=None, pages: int = -1, code: int = 200):
    if additional is None:
        additional = {}

    returning = {
        'code': 1,
        'data': data,
        **additional
    }
    if pages != -1:
        returning['pages'] = pages

    return response(returning, code)


def fail(error: str, additional=None, code: int = 400):
    if additional is None:
        additional = {}
    return response({
        'code': 0,
        'key': error,
        'message': ERRORS[error],
        **additional
    }, code)


def created():
    return success({}, code=201)


def no_content():
    return success({}, code=204)
