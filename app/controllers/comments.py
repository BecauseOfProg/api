import time
from pony.orm import *

from app.models.comment import Comment


class CommentsController:
    @staticmethod
    def fill_information(comment: Comment, to_exclude=None):
        print(to_exclude)
        return comment.to_dict(exclude=to_exclude)

    @staticmethod
    @db_session
    def multi_fill_information(comments: [Comment], to_exclude=None):
        comments = list(comments)
        for comment in comments:
            print(comment)
            comments[comments.index(comment)] = CommentsController.fill_information(comment, to_exclude)
        return comments

    @staticmethod
    @db_session
    def fetch_all():
        return Comment.select().sort_by(desc(Comment.timestamp)).sort_by(desc(Comment.pinned))

    @staticmethod
    @db_session
    def fetch_by_post(post):
        return CommentsController.fetch_all().filter(post=post, is_validated=True)

    @staticmethod
    @db_session
    def get_all():
        return CommentsController.multi_fill_information(CommentsController.fetch_all())

    @staticmethod
    @db_session
    def create_one(params):
        timestamp = int(time.time())
        slug = f"{params['username']}-{str(timestamp)}"
        comment = Comment(slug=slug,
                          username=params['username'],
                          email=params['email'],
                          ip=params['ip'],
                          post=params['post'],
                          content=params['content'],
                          timestamp=timestamp)
        commit()
        return True

    @staticmethod
    @db_session
    def validate_one(comment):
        comment = Comment[comment]
        comment.is_validated = True
        commit()

    @staticmethod
    @db_session
    def delete_one(url):
        Comment[url].delete()
        return True
