import mongoengine as mongodb


class Post(mongodb.DynamicDocument):
    title = mongodb.StringField(required=True, min_length=5, max_length=64)
    post_id = mongodb.LongField(required=True)
    url = mongodb.StringField(required=True, min_length=5, max_length=64)
    category = mongodb.StringField(required=True, max_length=20)
    banner = mongodb.StringField(default="")
    content = mongodb.StringField(required=True, min_length=50)
    author = mongodb.StringField(required=True)
    timestamp = mongodb.IntField(required=True)
    meta = {"collection": "posts"}
