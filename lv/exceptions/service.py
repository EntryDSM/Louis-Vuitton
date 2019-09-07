class WrongDataException(Exception):
    pass


class WrongClassificationDataException(WrongDataException):
    pass


class WrongDocumentDataException(WrongDataException):
    pass


class WrongDiligenceGradeDataException(WrongDataException):
    pass


class WrongGedGradeDataException(WrongDataException):
    pass


class WrongAcademicGradeDataException(WrongDataException):
    pass


class NotAllowedValueException(Exception):
    pass


class DataSourceException(Exception):
    pass


class DataSourceFailureException(DataSourceException):
    pass


class NonExistDataException(DataSourceException):
    pass
