class WrongDataException(Exception):
    pass


class WrongClassificationDataException(WrongDataException):
    pass


class WrongDocumentDataException(WrongDataException):
    pass


class NotAllowedValueException(Exception):
    pass
