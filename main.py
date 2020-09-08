from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_cors import CORS
from core.database import ApiDatabase

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
db = ApiDatabase.create()

from app.views import errors, posts, auth, users, blog_posts, comments

db.generate_mapping()
