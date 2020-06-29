class DataError(Exception):
    def __init__(self, required_data, optional_data):
        self.required_data = required_data
        self.optional_data = optional_data


class NotUnique(Exception):
    pass


class InvalidCredentials(Exception):
    pass


class PaginationError(Exception):
    pass
