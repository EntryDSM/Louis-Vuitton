class ExternalServiceException(Exception):
    ...


class InterCallException(ExternalServiceException):
    ...


class InterCallBadRequestException(InterCallException):
    ...


class InterCallNotFoundException(InterCallException):
    ...


class ExternalServiceDownException(ExternalServiceException):
    ...
