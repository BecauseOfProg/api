from flask import Flask
from core.database import Database

app = Flask(__name__)
db = Database()

from app.views import errors, posts, sessions, users
