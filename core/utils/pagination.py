import math

from pony.orm import db_session

from core.exceptions import PaginationError


@db_session
def paginate(request, posts):
    try:
        page = request.args.get('page', '1')
        page = int(page)
        if page < 1:
            raise ValueError
    except ValueError:
        raise PaginationError
    pages = math.ceil(len(posts) / 10)
    posts = posts.page(page)
    return posts, pages
