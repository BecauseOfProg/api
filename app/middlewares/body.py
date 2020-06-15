from core.exceptions import DataError


class CheckBody:
    @staticmethod
    def call(request, required_data, optional_data):
        request_data = request.json
        parsed_data = {
            'optional': {}
        }
        for field in required_data:
            if field in request_data:
                parsed_data[field] = request_data[field]
            else:
                raise DataError

        for field in optional_data:
            if field in request_data:
                parsed_data['optional'][field] = request_data[field]

        return parsed_data
