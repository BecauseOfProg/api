from pony.orm import *
from main import db


class User(db.Entity):
    username = PrimaryKey(str, max_len=32)
    email = Required(str, unique=True)
    password = Required(str)
    password_type = Required(str, default="argon2")
    timestamp = Required(int)
    displayname = Required(str, max_len=32)
    avatar = Required(str, default="https://cdn.becauseofprog.fr/pictures/new_member.png", column='picture')
    description = Required(str, default="Bonjour ! :)")
    biography = Optional(str, column='bio')
    location = Optional(str, column='localisation')
    socials = Required(Json, default=[])
    permissions = Required(Json, default=[])
    is_email_public = Required(bool, column='mail_profile', default=False)
    token = Required(str)
    is_activated = Required(bool, default=True)

    _table_ = "users"
