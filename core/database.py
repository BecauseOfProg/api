from pony.orm import *

from .config import Config


class ApiDatabase:
    @staticmethod
    def create():
        config = Config()
        database = Database()
        database.bind(
            provider='mysql',
            host=config.get('db', 'host'),
            user=config.get('db', 'username'),
            passwd=config.get('db', 'password'),
            db=config.get('db', 'db')
        )
        return database
