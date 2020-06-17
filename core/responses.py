def response(data, code=200):
    return data, code, {'Content-Type': 'application/json'}


def no_content():
    return response('', 204)
