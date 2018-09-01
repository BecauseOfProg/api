from core.exceptions import DataError


class CheckBody:
    def __init__(self, request, required_data):
        request_data = request.json
        for field in required_data:
            if field in request_data:
                pass
            else:
                raise DataError
