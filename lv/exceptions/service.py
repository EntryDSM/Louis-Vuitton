class WrongDataException(Exception):
    ...


class WrongClassificationDataException(WrongDataException):
    ...


class WrongDocumentDataException(WrongDataException):
    ...


class NotAllowedValueException(Exception):
    ...


class ExternalServiceException(Exception):
    ...


class InterCallException(Exception):
    ...


class InterCallBadRequestException(InterCallException):
    ...


class InterCallNotFoundException(InterCallException):
    ...
