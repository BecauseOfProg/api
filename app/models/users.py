from pony.orm import *
from main import db


class User(db.Entity):
    username = PrimaryKey(str, max_len=32)
    displayname = Required(str, max_len=32)
    email = Required(str, unique=True)
    password = Required(str)
    password_type = Required(str, default='argon2')
    permissions = Required(Json, default=[])
    token = Required(str)
    timestamp = Required(int)
    picture = Required(str, default='https://cdn.becauseofprog.fr/v2/sites/becauseofprog.fr/pictures/new_member.png')
    description = Optional(str)
    biography = Optional(str)
    location = Optional(str)
    socials = Required(Json, default=[])
    is_email_public = Required(bool, default=False)
    is_activated = Required(bool, default=True)
    is_verified = Required(bool, default=False)

    _table_ = 'users'
