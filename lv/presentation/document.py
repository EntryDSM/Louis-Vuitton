from sanic import Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView

from lv.data.repositories.document import AttachedDocumentRepository
from lv.exceptions.http import BadRequestParameter
from lv.exceptions.service import WrongDocumentDataException
from lv.presentation.helper import as_response, check_submit_status
from lv.services.document import (
    get_attached_documents,
    upsert_attached_documents,
)

bp_document = Blueprint("document")


class ApplicantAttachedDocumentView(HTTPMethodView):
    document_repository = AttachedDocumentRepository()

    @check_submit_status
    async def get(self, _: Request, email: str) -> HTTPResponse:
        documents = await get_attached_documents(
            email, self.document_repository
        )

        return json(status=200, body=as_response(documents))

    @check_submit_status
    async def patch(self, request: Request, email: str) -> HTTPResponse:
        try:
            await upsert_attached_documents(
                email, self.document_repository, request.json
            )
        except WrongDocumentDataException:
            raise BadRequestParameter('Invalid document value')

        return HTTPResponse(status=204)


bp_document.add_route(
    ApplicantAttachedDocumentView.as_view(), '/document'
)
