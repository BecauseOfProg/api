import time

from pony.orm import *
from werkzeug.exceptions import NotFound

from app.controllers.users import UsersController
from app.models.posts import Post


class PostsController:
    @staticmethod
    def fill_information(post: Post, additional_fields=None):
        if additional_fields is None:
            additional_fields = []

        fields = ['title', 'url', 'category', 'author', 'timestamp', 'banner'] + additional_fields
        post = post.to_dict(only=fields)
        post['author'] = UsersController.get_one(post['author'])
        return post

    @staticmethod
    @db_session
    def get_all():
        posts = list(Post.select().order_by(desc(Post.timestamp)))
        for post in posts:
            posts[posts.index(post)] = PostsController.fill_information(post)
        return posts

    @staticmethod
    @db_session
    def get_last():
        posts = list(Post.select().order_by(desc(Post.timestamp)))
        return PostsController.fill_information(posts[0])

    @staticmethod
    @db_session
    def get_one(url):
        try:
            return PostsController.fill_information(Post[url], ['content'])
        except core.ObjectNotFound:
            raise NotFound

    @staticmethod
    @db_session
    def create_one(title, url, category, content, banner, author_username):
        timestamp = int(time.time())
        post = Post(title=title,
                    url=url,
                    content=content,
                    category=category,
                    banner=banner,
                    timestamp=timestamp,
                    author=author_username)
        commit()
        return True

    @staticmethod
    @db_session
    def update_one(url, params, optional_data):
        try:
            post = Post[url]
            for field in optional_data:
                if field in params:
                    setattr(post, field, params[field])
            commit()
        except core.ObjectNotFound:
            raise NotFound

    @staticmethod
    @db_session
    def delete_one(url):
        try:
            Post[url].delete()
            return True
        except core.ObjectNotFound:
            raise NotFound
