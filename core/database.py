import mongoengine as mongodb

from .config import Config


class Database:

    def __init__(self):
        self.config = Config()
        self.db = self.config.get("db", "db")
        self.host = self.config.get("db", "host")
        self.port = self.config.get("db", "port")
        self.username = self.config.get("db", "username")
        self.password = self.config.get("db", "password")
        self.auth_source = self.config.get("db", "auth_source")
        mongodb.connect(db=self.db,
                        host=self.host,
                        port=int(self.port),
                        username=self.username,
                        password=self.password,
                        authentication_source=self.auth_source)
