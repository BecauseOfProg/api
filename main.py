from flask import Flask
from flask_cors import CORS
from core.database import ApiDatabase

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
db = ApiDatabase.create()

from app.views import errors, posts, auth, users, blog_posts

db.generate_mapping()
