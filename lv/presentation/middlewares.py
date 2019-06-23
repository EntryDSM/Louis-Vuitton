from sanic import Sanic
from sanic.config import Config
from sanic.exceptions import SanicException
from sanic.request import Request
from sanic.response import HTTPResponse, json

from ..data.db.mysql import MySQLClient


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
        'autocommit': True,
    }


async def init_data_clients(app: Sanic, _) -> None:
    await MySQLClient.init(generate_db_config(app.config))
    # AsyncHTTPClient.init()


# Todo
# async def close_data_clients(app: Sanic, _) -> None:
#     # mysql connection destroy
#     pass


async def error_handler(_: Request, exception: SanicException) -> HTTPResponse:
    return json(
        status=exception.status_code,
        body={
            'message': exception.args[0]
        }
    )
