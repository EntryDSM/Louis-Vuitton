from sanic.exceptions import add_status_code, SanicException


@add_status_code(400)
class BadRequestParameter(SanicException):
    ...


@add_status_code(403)
class Forbidden(SanicException):
    ...


@add_status_code(404)
class NotFoundApplicant(SanicException):
    ...


@add_status_code(500)
class InternalServerError(SanicException):
    ...
