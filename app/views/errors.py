import json

from main import app


@app.errorhandler(400)
def client_error(error):
    response = json.dumps({
        "code": 0,
        "message": "Bad request"
    })
    return (response, 400, {"Content-Type": "application/json"})


@app.errorhandler(401)
def unauthorized(error):
    response = {
        "code": 0,
        "message": "Unauthorized"
    }
    return (json.dumps(response), 401, {"Content-Type": "application/json"})


@app.errorhandler(403)
def forbidden(error):
    response = {
        "code": 0,
        "message": "Forbidden"
    }
    return (json.dumps(response), 403, {"Content-Type": "application/json"})


@app.errorhandler(404)
def page_not_found(error):
    response = {
        "code": 0,
        "message": "Not found"
    }
    return (json.dumps(response), 404, {"Content-Type": "application/json"})


@app.errorhandler(405)
def method_not_allowed(error):
    response = {
        "code": 0,
        "message": "Method not allowed"
    }
    return (json.dumps(response), 405, {"Content-Type": "application/json"})


@app.errorhandler(500)
def internal_server_error(error):
    response = {
        "code": 0,
        "message": "Internal server error"
    }
    return (json.dumps(response), 500, {"Content-Type": "application/json"})
