from random import randint
from time import time


def generate_id():
    timestamp = str(int(time()))
    random_number = str(randint(0, 999))
    return int(timestamp + random_number)
