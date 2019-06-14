from sanic import Blueprint
from sanic.request import Request


bp_classification = Blueprint("classification")


@bp_classification.get('/classification')
async def get_applicant_classification(_: Request):
    pass


@bp_classification.patch('/classification')
async def patch_applicant_classification(_: Request):
    pass
