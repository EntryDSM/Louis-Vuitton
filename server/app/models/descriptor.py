import datetime


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
        if default:
            if not isinstance(default, int):
                raise ValueError(f"int was expected for default but {type(default)} was given")
            if self.unsigned:
                if default < 0:
                    raise ValueError("expected positive for default but negative was given")
        super(Integer, self).__init__(default)

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise ValueError(f"int was expected but {type(value)} was given")
        if self.unsigned:
            if value < 0:
                raise ValueError("expected positive but negative was given")
        super(Integer, self).__set__(instance, value)


class Float(Type):
    def __init__(self, unsigned=False, default=None):
        self.unsigned = unsigned
        if default:
            if not isinstance(default, float):
                raise ValueError(f"int was expected for default but {type(default)} was given")
            if self.unsigned:
                if default < 0:
                    raise ValueError("positive was expected but negative was given")
        super(Float, self).__init__(default)

    def __set__(self, instance, value):
        if not isinstance(value, float):
            raise ValueError(f"int was expected for default but {type(value)} was given")
        if self.unsigned:
            if value < 0:
                raise ValueError("positive was expected but negative was given")
        super(Float, self).__set__(instance, value)


class String(Type):
    def __init__(self, length=0, default=None):
        self.length = length
        if default:
            if not isinstance(default, str):
                raise ValueError(f"str was expected for default but {type(default)} was given")
            if self.length and (len(default) > self.length):
                raise ValueError(f"maximum length is {self.length} but given string's length is {len(default)}")
        super(String, self).__init__(default)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise ValueError(f"str was expected for default but {type(value)} was given")
        if self.length and (len(value) > self.length):
            raise ValueError(f"maximum length is {self.length} but given string's length is {len(value)}")
        super(String, self).__set__(instance, value)


class Enum(Type):
    def __init__(self, keys, default=None):
        self.keys = keys
        if default and default not in keys:
            raise ValueError(f"default value must be one of {self.keys} but '{default}' was given")
        super(Enum, self).__init__(default)

    def __set__(self, instance, value):
        if value not in self.keys:
            raise ValueError(f"value must be one of {self.keys} but '{value}' was given")
        super(Enum, self).__set__(instance, value)


class Bool(Type):
    def __init__(self, default=None):
        if default:
            if not isinstance(default, bool):
                raise ValueError(f"bool was expected for default but {type(default)} was given")
        super(Bool, self).__init__(default)

    def __set__(self, instance, value):
        if not isinstance(value, bool):
            raise ValueError(f"bool was expected  but {type(value)} was given")
        super(Bool, self).__set__(instance, value)


class TimeStamp(Type):
    def __init__(self, default=None):
        if default:
            if not isinstance(default, datetime.datetime):
                raise ValueError(f"datetime was expected for default but {type(default)} was given")
            if callable(default):
                default = default()
        super(TimeStamp, self).__init__(default)

    def __set__(self, instance, value):
        if not isinstance(value, datetime.datetime):
            raise ValueError(f"datetime was expected but {type(value)} was given")
        super(TimeStamp, self).__set__(instance, value)


class Date(Type):
    def __init__(self, default=None):
        if default:
            if not isinstance(default, datetime.date):
                raise ValueError(f"date was expected for default but {type(default)} was given")
            if callable(default):
                default = default()
            super(Date, self).__init__(default)

    def __set__(self, instance, value):
        if not isinstance(value, datetime.date):
            raise ValueError(f"date was expected but {type(value)} was given")