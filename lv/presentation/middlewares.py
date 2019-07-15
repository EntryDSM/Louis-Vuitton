import decimal

from sanic import Sanic
from sanic.config import Config
from sanic.exceptions import SanicException
from sanic.request import Request
from sanic.response import HTTPResponse, json

from lv.data.db.mysql import MySQLClient
from lv.data.external_service.http import HTTPClient

ROUND_HALF_UP = 'ROUND_HALF_UP'


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
    await HTTPClient.init()


async def close_data_clients(_: Sanic, __) -> None:
    await MySQLClient.destroy()
    await HTTPClient.destroy()


async def change_rounding_mode(_: Sanic, __) -> None:
    decimal.getcontext().rounding = ROUND_HALF_UP


async def error_handler(_: Request, exception: SanicException) -> HTTPResponse:
    return json(
        status=exception.status_code,
        body={
            'message': exception.args[0]
        }
    )
