from sanic.exceptions import add_status_code, SanicException


@add_status_code(400)
class BadRequestParameter(SanicException):
    pass
