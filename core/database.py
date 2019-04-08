from pony.orm import *

from .config import Config


class ApiDatabase:

    @staticmethod
    def create():
        config = Config()
        db = config.get('db', 'db')
        host = config.get('db', 'host')
        username = config.get('db', 'username')
        password = config.get('db', 'password')
        database = Database()
        database.bind(provider='mysql',
                           host=host,
                           user=username,
                           passwd=password,
                           db=db)
        return database
