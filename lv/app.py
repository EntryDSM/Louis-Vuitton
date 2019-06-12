import os

from sanic import Sanic

from lv.conf import (
    Config,
    Development,
    Production,
    Testing,
)
from lv.vault import get_config
from lv.presentation.middlewares import (
    init_data_clients,
    LISTENER_TYPE,
)


def init_config(env: str) -> Config:
    mapping = {
        'default': Config,
        'testing': Testing,
        'development': Development,
        'production': Production,
    }

    config = mapping[env](**get_config(env))
    check_env_type(config)

    return config


def check_env_type(config: Config):
    if config.env == 'production' and config.DEBUG:
        raise RuntimeError('You should set DEBUG to false in production')


def create_app() -> Sanic:
    _app = Sanic(__name__)

    _app.config.from_object(init_config(os.getenv('RUN_ENV', 'default')))
    _app.register_listener(init_data_clients, LISTENER_TYPE[0])

    return _app
