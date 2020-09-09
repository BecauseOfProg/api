from pony.orm import *
from main import db


class Post(db.Entity):
    url = PrimaryKey(str, max_len=64)
    title = Required(str, max_len=64)
    category = Required(str, max_len=20)
    banner = Optional(str, default='')
    content = Required(str)
    author = Required(str)
    timestamp = Required(int, unique=True)

    _table_ = 'posts'
