from sanic import Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView

from lv.data.repositories.classification import ClassificationRepository
from lv.exceptions.http import BadRequestParameter
from lv.exceptions.service import WrongClassificationDataException
from lv.presentation.helper import check_submit_status
from lv.services.classification import (
    get_applicant_classification,
    upsert_applicant_classification,
)

bp_classification = Blueprint("classification")


class ApplicantClassificationView(HTTPMethodView):
    classification_repository = ClassificationRepository()

    @check_submit_status
    async def get(self, _: Request, email: str) -> HTTPResponse:
        classification = await get_applicant_classification(
            email, self.classification_repository
        )

        return json(status=200, body=classification)

    @check_submit_status
    async def patch(self, request: Request, email: str) -> HTTPResponse:
        try:
            await upsert_applicant_classification(
                email, self.classification_repository, request.json
            )
        except WrongClassificationDataException:
            raise BadRequestParameter('Invalid classification value')

        return HTTPResponse(status=200)


bp_classification.add_route(
    ApplicantClassificationView.as_view(), '/classification'
)
