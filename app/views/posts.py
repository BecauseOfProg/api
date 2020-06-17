from flask import request

from app.controllers.posts import PostsController
from app.controllers.users import UsersController
from app.middlewares.body import CheckBody
from app.middlewares.permissions import CheckPermissions
from core import responses
from core.utils.pagination import paginate
from main import app


@app.route('/v1/posts', methods=['GET'])
def get_all_posts():
    posts = PostsController.fetch_all()
    posts, pages = paginate(request, posts)
    return responses.response({
        'code': 1,
        'pages': pages,
        'data': PostsController.multi_fill_information(posts)
    })


@app.route('/v1/posts/last', methods=['GET'])
def get_last_post():
    return responses.response({
        'code': 1,
        'data': PostsController.get_last()
    })


@app.route('/v1/posts/<string:url>', methods=['GET'])
def get_one_post(url):
    return responses.response({
        'code': 1,
        'data': PostsController.get_one(url)
    })


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
        },
        'banner': {
            'type': 'string'
        }
    }
    data = CheckBody.call(request, required_data=required_data)
    CheckPermissions(request, permissions=['POST_WRITE'])
    author = UsersController.get_one_by_token(request.headers.get('Authorization'))
    PostsController.create_one(title=data['title'],
                               url=data['url'],
                               category=data['category'],
                               content=data['content'],
                               author_username=author['username'],
                               banner=data['banner'])
    return responses.created()


@app.route('/v1/posts/<string:url>', methods=['PATCH'])
def edit_post(url):
    optional_data = {
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
    PostsController.get_one(url)
    data = CheckBody.call(request, optional_data=optional_data)
    CheckPermissions(request, permissions=['POST_WRITE'])
    PostsController.update_one(url=url,
                               params=data['optional'],
                               optional_data=optional_data)
    return responses.no_content()


@app.route('/v1/posts/<string:url>', methods=['DELETE'])
def delete_post(url):
    CheckPermissions(request, permissions=['POST_WRITE'])
    PostsController.delete_one(url)
    return responses.no_content()
