import time

from pony.orm import *
from werkzeug.exceptions import NotFound
from core.exceptions import DataError

from app.controllers.users import UsersController
from app.models.posts import Post
from core.utils import ids


class PostsController:
    @staticmethod
    def fill_informations(post: Post, additional_fields: list = []):
        fields = ['title', 'url', 'category', 'author', 'timestamp', 'banner'] + additional_fields
        post = post.to_dict(only=fields)
        post['author'] = UsersController.get_one(post['author'])
        return post

    @staticmethod
    @db_session
    def get_all():
        posts = list(Post.select().order_by(desc(Post.timestamp)))
        for post in posts:
            posts[posts.index(post)] = PostsController.fill_informations(post)
        return posts

    @staticmethod
    @db_session
    def get_last():
        posts = list(Post.select().order_by(desc(Post.timestamp)))
        return PostsController.fill_informations(posts[0])

    @staticmethod
    @db_session
    def get_one(url):
        try:
            return PostsController.fill_informations(Post[url], ['content'])
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
    def update_one(url, params):
        try:
            post = Post[url]
            post.title = params['title']
            post.category = params['category']
            post.content = params['content']
            post.banner = params['banner']
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
