def response(data, code=200):
    return data, code, {'Content-Type': 'application/json'}


def created():
    return response({'code': 1}, 201)


def no_content():
    return response('', 204)
