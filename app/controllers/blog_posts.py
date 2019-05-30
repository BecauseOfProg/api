import time

from pony.orm import *
from werkzeug.exceptions import NotFound
from app.controllers.users import UsersController
from app.models.blog_posts import BlogPost


class BlogPostsController:
    @staticmethod
    def fill_informations(post: BlogPost, without_content: bool = False):
        if without_content:
            to_exclude = 'content'
        else:
            to_exclude = None
        p = post.to_dict(exclude=to_exclude)
        p['author'] = UsersController.get_one(p['author'])
        return p

    @staticmethod
    @db_session
    def get_all():
        posts = list(BlogPost.select().order_by(desc(BlogPost.timestamp)))
        for post in posts:
            posts[posts.index(post)] = BlogPostsController.fill_informations(post, True)
        return posts

    @staticmethod
    @db_session
    def get_last():
        posts = list(BlogPost.select().order_by(desc(BlogPost.timestamp)))
        return BlogPostsController.fill_informations(posts[0])

    @staticmethod
    @db_session
    def get_one(url):
        try:
            return BlogPostsController.fill_informations(BlogPost[url])
        except core.ObjectNotFound:
            raise NotFound

    @staticmethod
    @db_session
    def create_one(params, optional_data):
        timestamp = int(time.time())

        # Required fields
        post = BlogPost(url=params['url'],
                        title=params['title'],
                        timestamp=timestamp,
                        author=params['author_username'],
                        type=params['type'],
                        category=params['category'],
                        description=params['description'],
                        labels=params['labels'],
                        banner=params['banner'],
                        content=params['content'])
        # Optional fields
        for field in optional_data:
            if field in params['optional']:
                setattr(post, field, params['optional'][field])
        commit()
        return True

    @staticmethod
    @db_session
    def update_one(url, params, optional_data):
        try:
            post = BlogPost[url]
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
            BlogPost[url].delete()
            return True
        except core.ObjectNotFound:
            raise NotFound
