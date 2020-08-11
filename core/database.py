import os
from pony.orm import *


class ApiDatabase:
    @staticmethod
    def create():
        database = Database()
        database.bind(
            provider='mysql',
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            passwd=os.getenv('DB_PASSWORD'),
            db=os.getenv('DB')
        )
        return database
