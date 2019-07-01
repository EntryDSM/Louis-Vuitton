import os

from sanic import Sanic
from sanic.exceptions import SanicException
from sanic.request import Request
from sanic.response import text

from lv.conf import (
    Config,
    Development,
    Production,
    Testing,
)
from lv.vault import get_config
from lv.presentation import api
from lv.presentation.middlewares import (
    close_data_clients,
    error_handler,
    init_data_clients,
)


BEFORE_SERVER_START = 'before_server_start'
AFTER_SERVER_STOP = 'after_server_stop'


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
    _app.register_listener(init_data_clients, BEFORE_SERVER_START)
    _app.register_listener(close_data_clients, AFTER_SERVER_STOP)
    _app.error_handler.add(SanicException, error_handler)
    _app.blueprint(api)

    @_app.get('/')
    async def _(_: Request):
        return text('ping')

    return _app
