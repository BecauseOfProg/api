import mongoengine as mongodb


class User(mongodb.DynamicDocument):
    email = mongodb.EmailField(required=True, min_length=6)
    user_id = mongodb.LongField(required=True)
    password = mongodb.StringField(required=True, min_length=8)
    timestamp = mongodb.IntField(required=True)
    username = mongodb.StringField(required=True, min_length=2, max_length=32)
    displayname = mongodb.StringField(required=True, min_length=2, max_length=32)
    avatar = mongodb.StringField(default="https://cdn.becauseofprog.fr/pictures/new_member.png")
    description = mongodb.StringField(required=False)
    biography = mongodb.StringField(required=False)
    location = mongodb.StringField(required=False)
    socials = mongodb.ListField(required=False)
    permissions = mongodb.ListField(required=False)
    is_email_public = mongodb.BooleanField(default=False)
    token = mongodb.StringField(required=True)
    is_activated = mongodb.BooleanField(default=True)
    meta = {"collection": "users"}
