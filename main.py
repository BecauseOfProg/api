from flask import Flask
from core.database import ApiDatabase

app = Flask(__name__)
db = ApiDatabase.create()

from app.views import errors, posts, auth, users, arduino

db.generate_mapping()
