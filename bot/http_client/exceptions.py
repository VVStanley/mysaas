class HttpException(Exception):
    pass


class NotFoundException(HttpException):
    pass


class APIException(HttpException):
    pass


class ModelValidateException(HttpException):
    pass
