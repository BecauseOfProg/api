from pony.orm import *
from main import db


class ArduinoProject(db.Entity):
    url = PrimaryKey(str, max_len=64)
    author = Required(str)
    name = Required(str, max_len=64)
    summary = Required(str, max_len=250)
    illustration = Optional(str, default='')
    video = Optional(str, default='')
    link = Optional(str, default='')
    description = Optional(str, default='')
    timestamp = Required(int)
    thumbs_up = Required(Json, default=[])
    is_from_staff = Required(bool, default=False)
    is_featured = Required(bool, default=False)

    _table_ = 'arduino'
