import time

from werkzeug.exceptions import NotFound
from mongoengine.errors import ValidationError
from core.exceptions import DataError

from app.controllers.users import UsersController
from app.models.posts import Post
from core.utils import ids


class PostsController:
    @staticmethod
    def fill_informations(post):
        response = {
            "post_id": post.post_id,
            "timestamp": post.timestamp,
            "title": post.title,
            "url": post.url,
            "category": post.category,
            "author": UsersController.get_one(post.author),
            "content": post.content
        }
        if post.banner != "":
            response.update({
                "banner": post.banner
            })
        return response

    @staticmethod
    def get_all():
        posts = []
        for post in Post.objects:
            posts.append(PostsController.fill_informations(post))
        return posts

    @staticmethod
    def get_one(url):
        posts = {}
        for post in Post.objects(url=url):
            posts = PostsController.fill_informations(post)
        if posts == {}:
            raise NotFound
        else:
            return posts

    @staticmethod
    def create_one(title, url, category, content, author_username):
        try:
            timestamp = int(time.time())
            post_id = ids.generate_id()
            post = Post(title=title, url=url, content=content,
                        category=category, timestamp=timestamp, post_id=post_id, author=author_username)
            post.save()
            return True
        except ValidationError:
            raise DataError

    @staticmethod
    def update_one(url, params):
        try:
            Post.objects(url=url).update_one(set__title=params["title"],
                                             set__category=params["category"], set__content=params["content"],
                                             set__banner=params["banner"])
            return True
        except ValidationError:
            raise DataError

    @staticmethod
    def delete_one(url):
        post = PostsController.get_one(url)
        if post == {}:
            raise NotFound
        else:
            Post.objects(url=url).delete()
            return True
