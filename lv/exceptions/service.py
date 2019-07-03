class WrongDataException(Exception):
    ...


class WrongClassificationDataException(WrongDataException):
    ...


class WrongDocumentDataException(WrongDataException):
    ...


class NotAllowedValueException(Exception):
    ...


class DataSourceException(Exception):
    ...


class DataSourceFailureException(DataSourceException):
    ...


class NonExistDataException(DataSourceException):
    ...
