from sanic import Sanic
from sanic.config import Config

from ..data.db import MySQLClient


LISTENER_TYPE = (
    'before_server_start',
    'after_server_start',
    'before_server_stop',
    'after_server_stop',
)


def generate_db_config(config: Config) -> dict:
    return {
        'user': config.DATABASE_USERNAME,
        'db': config.DATABASE_NAME,
        'host': config.DATABASE_HOST,
        'password': config.DATABASE_PASSWORD,
    }


async def init_data_clients(app: Sanic, _) -> None:
    await MySQLClient.init(generate_db_config(app.config))
    # AsyncHTTPClient.init()
