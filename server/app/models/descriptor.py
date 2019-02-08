class Type:
    name: str

    def __init__(self, default):
        self.default = default

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name, self.default)

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


class Integer(Type):
    def __init__(self, unsigned=False, default=None):
        self.unsigned = unsigned
        super().__init__(default)

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise ValueError("value is not int")
        if self.unsigned:
            if value < 0:
                raise ValueError("negative value for unsigned type")
        super().__set__(instance, value)


class Float(Type):
    def __init__(self, unsigned=False, default=None):
        self.unsigned = unsigned
        super().__init__(default)

    def __set__(self, instance, value):
        if not isinstance(value, float):
            raise ValueError("value is not float")
        if self.unsigned:
            if value < 0:
                raise ValueError("negative value for unsigned type")
        super().__set__(instance, value)


class String(Type):
    def __init__(self, length=0):
        self.length = 0

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise ValueError("value is not str")
        if self.length and (len(value) > self.length):
            raise ValueError("value too long")
        super().__set__(instance, value)


class Enum(Type):
    def __init__(self, *args):
        self.keys = args

    def __set__(self, instance, value):
        if value not in self.keys:
            raise ValueError(f"Value '{value}' is not in enum key list {self.keys}")
        super().__set__(instance, value)

