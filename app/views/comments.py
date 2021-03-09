from flask import request

from core import responses
from core.utils.pagination import paginate
from app.controllers.blog_posts import BlogPostsController
from app.controllers.comments import CommentsController
from app.middlewares.body import CheckBody
from app.middlewares.permissions import CheckPermissions
from main import app


@app.route('/v1/comments', methods=['GET'])
def get_all_comments():
    CheckPermissions.call(request, ['USER_WRITE'])

    comments = CommentsController.fetch_all()
    comments, pages = paginate(request, comments)
    comments = CommentsController.multi_fill_information(comments)
    return responses.success(comments, pages=pages)


@app.route('/v1/comments/<string:post>', methods=['GET'])
def get_comments_by_post(post):
    BlogPostsController.get_one(post)
    comments = CommentsController.fetch_by_post(post)
    comments, pages = paginate(request, comments)
    return responses.success(
        CommentsController.multi_fill_information(comments, to_exclude=['ip', 'is_validated', 'email']),
        pages=pages
    )


@app.route('/v1/comments/<string:post_url>', methods=['POST'])
def create_comment(post_url):
    required_data = {
        'username': {
            'type': 'string',
            'min_length': 2,
            'max_length': 64
        },
        'email': {
            'type': 'string'
        },
        'content': {
            'type': 'string',
            'min_length': 5,
            'max_length': 500
        }
    }
    BlogPostsController.get_one(post_url)
    data = CheckBody.call(request, required_data=required_data)
    data['post'] = post_url
    data['ip'] = request.remote_addr
    CommentsController.create_one(data)

    return responses.no_content()


@app.route('/v1/comments/<string:post>/<string:comment>', methods=['PUT'])
def validate_comment(post, comment):
    CheckPermissions.call(request, ['USER_WRITE'])
    CommentsController.validate_one(comment)
    return responses.no_content()


@app.route('/v1/comments/<string:post>/<string:comment>', methods=['DELETE'])
def delete_comment(post, comment):
    CheckPermissions.call(request, ['USER_WRITE'])
    CommentsController.delete_one(comment)
    return responses.no_content()
