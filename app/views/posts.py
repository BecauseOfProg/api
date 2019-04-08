from flask import request

from app.controllers.posts import PostsController
from app.controllers.users import UsersController
from app.middlewares.body import CheckBody
from app.middlewares.permissions import CheckPermissions
from core import responses
from core.exceptions import DataError
from main import app


@app.route('/v1/posts', methods=['GET'])
def get_all_posts():
    response = {
        'code': 1,
        'posts': PostsController.get_all()
    }
    return responses.response(response)

@app.route('/v1/posts/last', methods=['GET'])
def get_last_post():
    response = {
        'code': 1,
        'post': PostsController.get_last()
    }
    return responses.response(response)

@app.route('/v1/posts/<string:url>', methods=['GET'])
def get_one_post(url):
    response = {
        'code': 1,
        'post': PostsController.get_one(url)
    }
    return responses.response(response)


@app.route('/v1/posts', methods=['POST'])
def create_post():
    required_data = {
        'title': {
            'type': 'string',
            'min_length': 5,
            'max_length': 64
        },
        'url': {
            'type': 'string',
            'min_length': 5,
            'max_length': 64
        },
        'category': {
            'type': 'string',
            'max_length': 20
        },
        'content': {
            'type': 'string',
            'min_length': 50
        }
    }
    try:
        CheckBody(request, required_data=required_data)
        CheckPermissions(request, permissions=['POST_WRITE'])
        request_data = request.json
        author = UsersController.get_one_by_token(request.headers.get('Authorization'))
        PostsController.create_one(title=request_data['title'],
                                   url=request_data['url'],
                                   category=request_data['category'],
                                   content=request_data['content'],
                                   author_username=author['username'])
        return responses.response({'code': 1})
    except DataError:
        return responses.data_error(required_data)

@app.route('/v1/posts/<string:url>', methods=['PATCH'])
def edit_post(url):
    required_data = {
        'title': {
            'type': 'string',
            'min_length': 5,
            'max_length': 64
        },
        'category': {
            'type': 'string',
            'max_length': 20
        },
        'banner': {
            'type': 'string'
        },
        'content': {
            'type': 'string',
            'min_length': 50
        }
    }
    try:
        PostsController.get_one(url)
        CheckBody(request, required_data=required_data)
        CheckPermissions(request, permissions=['POST_WRITE'])
        request_data = request.json
        PostsController.update_one(url=url,
                                   title=request_data['title'],
                                   category=request_data['category'],
                                   content=request_data['content'])
        return responses.response({'code': 1})
    except DataError:
        return responses.data_error(required_data)

@app.route('/v1/posts/<string:url>', methods=['DELETE'])
def delete_post(url):
    CheckPermissions(request, permissions=['POST_WRITE'])
    PostsController.delete_one(url)
    return responses.response({
        'code': 1
    })
