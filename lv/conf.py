from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    env: str
    APP_HOST: str
    APP_PORT: str

    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str

    HERMES_HOST: str = 'localhost:8888'

    SERVICE_NAME: str = 'entry_lv'
    DEBUG: bool = True
    TESTING: bool = False


@dataclass(frozen=True)
class Development(Config):
    DEBUG: bool = False


@dataclass(frozen=True)
class Production(Config):
    DEBUG: bool = False


@dataclass(frozen=True)
class Testing(Config):
    TESTING: bool = True

