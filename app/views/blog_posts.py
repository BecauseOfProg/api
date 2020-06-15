from flask import request

from app.controllers.blog_posts import BlogPostsController
from app.controllers.users import UsersController
from app.middlewares.body import CheckBody
from app.middlewares.permissions import CheckPermissions
from core import responses
from core.exceptions import DataError
from main import app


@app.route('/v1/blog-posts', methods=['GET'])
def get_all_blog_posts():
    try:
        page = request.args.get('page', '1')
        page = int(page)
    except ValueError:
        return responses.response({
            'code': 0,
            'message': 'Invalid page number. Required type : integer'
        }, 400)

    posts = BlogPostsController.get_all()

    category = request.args.get('category', None)
    if category is not None:
        posts = BlogPostsController.filter_by_category(posts, category)

    type = request.args.get('type', None)
    if type is not None:
        posts = BlogPostsController.filter_by_type(posts, type)

    (posts, pages) = BlogPostsController.paginate(posts, page)
    posts = BlogPostsController.multi_fill_information(posts)

    response = {
        'code': 1,
        'pages': pages,
        'data': posts
    }
    return responses.response(response)

@app.route('/v1/blog-posts/last', methods=['GET'])
def get_last_blog_post():
    response = {
        'code': 1,
        'data': BlogPostsController.get_last()
    }
    return responses.response(response)


@app.route('/v1/blog-posts', methods=['POST'])
def create_blog_post():
    required_data = {
        'url': {
            'type': 'string',
            'min_length': 5,
            'max_length': 64
        },
        'title': {
            'type': 'string',
            'min_length': 5,
            'max_length': 64
        },
        'type': {
            'type': 'string'
        },
        'category': {
            'type': 'string'
        },
        'description': {
            'type': 'string',
            'min_length': 10,
            'max_length': 250
        },
        'labels': {
            'type': 'list<string>'
        },
        'banner': {
            'type': 'string'
        },
        'content': {
            'type': 'string',
            'min_length': 20
        }
    }
    optional_data = {
        'locale': {
            'type': 'string',
            'default': 'fr'
        }
    }
    try:
        data = CheckBody.call(request, required_data=required_data, optional_data=optional_data)
        CheckPermissions(request, permissions=['BLOG_WRITE'])
        author = UsersController.get_one_by_token(request.headers.get('Authorization'))
        data['author_username'] = author['username']
        BlogPostsController.create_one(params=data,
                                     optional_data=optional_data
                                     )
        return responses.response({'code': 1}, 201)
    except DataError:
        return responses.data_error(required_data, optional_data)

@app.route('/v1/blog-posts/<string:url>', methods=['GET'])
def get_one_blog_post(url):
    response = {
        'code': 1,
        'data': BlogPostsController.get_one(url)
    }
    return responses.response(response)

@app.route('/v1/blog-posts/<string:url>', methods=['PATCH'])
def edit_blog_post(url):
    optional_data = {
        'title': {
            'type': 'string',
            'min_length': 5,
            'max_length': 64
        },
        'type': {
            'type': 'string'
        },
        'category': {
            'type': 'string'
        },
        'description': {
            'type': 'string',
            'min_length': 10,
            'max_length': 250
        },
        'labels': {
            'type': 'list<string>'
        },
        'banner': {
            'type': 'string'
        },
        'content': {
            'type': 'string',
            'min_length': 20
        }
    }
    try:
        post = BlogPostsController.get_one(url)
        data = CheckBody.call(request, required_data={}, optional_data=optional_data)
        CheckPermissions(request, permissions=['BLOG_WRITE'])
        BlogPostsController.update_one(url=url,
                                       params=data['optional'],
                                       optional_data=optional_data)
        return responses.no_content()
    except DataError:
        return responses.data_error({}, optional_data)

@app.route('/v1/blog-posts/<string:url>', methods=['DELETE'])
def delete_blog_post(url):
    post = BlogPostsController.get_one(url)
    CheckPermissions(request, permissions=['BLOG_WRITE'])
    BlogPostsController.delete_one(url)
    return responses.no_content()
