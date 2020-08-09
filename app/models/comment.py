from pony.orm import *
from main import db


class Comment(db.Entity):
    slug = PrimaryKey(str)
    username = Required(str, max_len=64)
    email = Required(str)
    ip = Required(str)
    post = Required(str)
    content = Required(str)
    is_validated = Required(bool, default=False)
    pinned = Required(bool, default=False)
    timestamp = Required(int)

    _table_ = 'comments'
