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


def fail(message: str, additional=None, code: int = 400):
    if additional is None:
        additional = {}
    return response({
        'code': 0,
        'message': message,
        **additional
    }, code)


def created():
    return success({}, code=201)


def no_content():
    return success({}, code=204)
