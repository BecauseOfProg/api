from pony.orm import *
from main import db


class BlogPost(db.Entity):
    url = PrimaryKey(str, max_len=64)
    title = Required(str, max_len=64)
    timestamp = Required(int)
    author = Required(str)
    type = Required(str)
    category = Required(str)
    description = Required(str, column='desc', max_len=250)
    labels = Required(Json, default=[])
    banner = Required(str)
    content = Required(str)
    locale = Required(str, default='fr')
    article_language = Required(str, default='md')

    _table_ = 'articles'
