from flask import request

from app.controllers.blog_posts import BlogPostsController
from app.controllers.users import UsersController
from app.middlewares.body import CheckBody
from app.middlewares.permissions import CheckPermissions
from core import responses
from core.utils.pagination import paginate
from main import app


@app.route('/v1/blog-posts', methods=['GET'])
def get_all_blog_posts():
    posts = BlogPostsController.fetch_all()

    category = request.args.get('category', None)
    if category is not None:
        posts = BlogPostsController.filter_by_category(posts, category)

    type = request.args.get('type', None)
    if type is not None:
        posts = BlogPostsController.filter_by_type(posts, type)

    search = request.args.get('search', None)
    if search is not None:
        posts = BlogPostsController.filter_by_search(posts, search)

    posts, pages = paginate(request, posts)
    posts = BlogPostsController.multi_fill_information(posts)

    return responses.success(posts, pages=pages)


@app.route('/v1/blog-posts/last', methods=['GET'])
def get_last_blog_post():
    return responses.success(BlogPostsController.get_last())


@app.route('/v1/blog-posts', methods=['POST'])
def create_blog_post():
    required_data = {
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
    data = CheckBody.call(request, required_data=required_data, optional_data=optional_data)
    CheckPermissions(request, permissions=['BLOG_WRITE'])
    author = UsersController.get_one_by_token(request.headers.get('Authorization'))
    data['author_username'] = author['username']
    BlogPostsController.create_one(params=data,
                                   optional_data=optional_data
                                   )
    return responses.created()


@app.route('/v1/blog-posts/<string:url>', methods=['GET'])
def get_one_blog_post(url):
    return responses.success(BlogPostsController.get_one(url))


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
    post = BlogPostsController.get_one(url)
    data = CheckBody.call(request, optional_data=optional_data)
    CheckPermissions(request, permissions=['BLOG_WRITE'])
    BlogPostsController.update_one(url=url,
                                   params=data['optional'],
                                   optional_data=optional_data)
    return responses.no_content()


@app.route('/v1/blog-posts/<string:url>', methods=['DELETE'])
def delete_blog_post(url):
    post = BlogPostsController.get_one(url)
    CheckPermissions(request, permissions=['BLOG_WRITE'])
    BlogPostsController.delete_one(url)
    return responses.no_content()
