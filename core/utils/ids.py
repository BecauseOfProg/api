from random import randint
from time import time
from core.utils.url import urlify


def generate_id():
    timestamp = str(int(time()))
    random_number = str(randint(0, 9999))
    return int(timestamp + random_number)


def generate_url(url):
    return "%s-%s" % (urlify(url), str(int(time()))[6:])
