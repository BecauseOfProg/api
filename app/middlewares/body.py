from core.exceptions import DataError


class CheckBody:
    @staticmethod
    def call(request, required_data=None, optional_data=None):
        if required_data is None:
            required_data = {}
        if optional_data is None:
            optional_data = {}

        request_data = request.json
        parsed_data = {
            'optional': {}
        }
        for field in required_data:
            if field in request_data:
                parsed_data[field] = request_data[field]
            else:
                raise DataError(required_data, optional_data)

        for field in optional_data:
            if field in request_data:
                parsed_data['optional'][field] = request_data[field]

        return parsed_data
