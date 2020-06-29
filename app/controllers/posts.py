import time
from pony.orm import *
from core.utils.ids import generate_url
from app.controllers.users import UsersController
from app.models.posts import Post


class PostsController:
    @staticmethod
    @db_session
    def fill_information(post: Post, include_content: bool = False):
        to_exclude = None if include_content else 'content'
        post = post.to_dict(exclude=to_exclude)
        post['author'] = UsersController.get_one(post['author'])
        return post

    @staticmethod
    @db_session
    def multi_fill_information(posts: [Post], include_content: bool = False):
        posts = list(posts)
        for post in posts:
            posts[posts.index(post)] = PostsController.fill_information(post, include_content)
        return posts

    @staticmethod
    @db_session
    def fetch_all():
        return Post.select().sort_by(desc(Post.timestamp))

    @staticmethod
    @db_session
    def get_last():
        posts = PostsController.fetch_all()
        return PostsController.fill_information(posts.first(), True)

    @staticmethod
    @db_session
    def get_one(url):
        return PostsController.fill_information(Post[url], True)

    @staticmethod
    @db_session
    def create_one(params):
        timestamp = int(time.time())
        post = Post(title=params['title'],
                    url=generate_url(params['title']),
                    content=params['content'],
                    category=params['category'],
                    banner=params['banner'],
                    timestamp=timestamp,
                    author=params['author_username'])
        commit()
        return True

    @staticmethod
    @db_session
    def update_one(url, params, optional_data):
        post = Post[url]
        for field in optional_data:
            if field in params:
                setattr(post, field, params[field])
        commit()

    @staticmethod
    @db_session
    def delete_one(url):
        Post[url].delete()
        return True
