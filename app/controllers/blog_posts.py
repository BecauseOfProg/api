import time
import json
from pony.orm import *
from core.utils.ids import generate_url
from app.controllers.users import UsersController
from app.models.blog_posts import BlogPost


class BlogPostsController:
    @staticmethod
    def fill_information(post: BlogPost, include_content: bool = False):
        to_exclude = None if include_content else 'content'
        post = post.to_dict(exclude=to_exclude)
        post['author'] = UsersController.get_one(post['author'])
        return post

    @staticmethod
    @db_session
    def multi_fill_information(posts: [BlogPost], include_content: bool = False):
        posts = list(posts)
        for post in posts:
            posts[posts.index(post)] = BlogPostsController.fill_information(post, include_content)
        return posts

    @staticmethod
    @db_session
    def fetch_all():
        return BlogPost.select().sort_by(desc(BlogPost.timestamp))

    @staticmethod
    @db_session
    def filter_by_category(posts, category):
        return posts.where(category=category)

    @staticmethod
    @db_session
    def filter_by_type(posts, type):
        return posts.where(type=type)

    @staticmethod
    @db_session
    def filter_by_author(posts, author):
        return posts.where(author=author)

    @staticmethod
    @db_session
    def filter_by_search(posts, search):
        query = search.lower()
        return posts.filter(
            lambda post: query in post.title.lower() or query in post.description.lower()
        )

    @staticmethod
    @db_session
    def get_last():
        posts = BlogPostsController.fetch_all()
        return BlogPostsController.fill_information(posts.first(), include_content=True)

    @staticmethod
    @db_session
    def get_random():
        post = BlogPost.select().random(1)[0]
        return BlogPostsController.fill_information(post, include_content=True)

    @staticmethod
    @db_session
    def get_one(url):
        return BlogPostsController.fill_information(BlogPost[url], include_content=True)

    @staticmethod
    @db_session
    def create_one(params, optional_data):
        timestamp = int(time.time())

        # Required fields
        post = BlogPost(url=generate_url(params['title']),
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
        post = BlogPost[url]
        for field in optional_data:
            if field in params:
                setattr(post, field, params[field])
        commit()

    @staticmethod
    @db_session
    def delete_one(url):
        BlogPost[url].delete()
        return True
