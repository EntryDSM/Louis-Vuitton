from dacite import from_dict
from sanic.request import Request
from sanic.response import HTTPResponse, json

from lv.entities.classification import Classification
from lv.services import classification


# '/<user_id>/classification'
async def post_classification(request: Request, email: str) -> HTTPResponse:
    classification_data = from_dict(
        data_class=Classification, data=request.json
    )

    await classification.post_classification(classification_data, email)

    return HTTPResponse(status=201)


# '/<user_id>/classification'
async def get_classification(request: Request, email: str):
    ...
