from sanic import Sanic, Blueprint
from sanic.request import Request
from sanic.response import text


def init_router(app: Sanic) -> None:
    app.blueprint(bp)


bp = Blueprint('fake')


@bp.get('/')
async def fake(_: Request):
    return text('ping')
