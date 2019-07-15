from sanic import Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView

from lv.data.repositories.grade import (
    DiligenceGradeRepository,
    GradeRepository,
)
from lv.presentation.helper import check_submit_status, ged_not_allowed
from lv.services.grade import (
    get_diligence_grade,
    upsert_diligence_grade,
)

bp_grade = Blueprint("grade", url_prefix="/grade")


class DiligenceGradeView(HTTPMethodView):
    diligence_repository = DiligenceGradeRepository()
    grade_repository = GradeRepository()

    @check_submit_status
    @ged_not_allowed
    def get(self, _: Request, email: str) -> HTTPResponse:
        diligence_grade = await get_diligence_grade(
            email, self.diligence_repository
        )

        return json(status=200, body=diligence_grade)

    @check_submit_status
    @ged_not_allowed
    def patch(self, request: Request, email: str) -> HTTPResponse:
        await upsert_diligence_grade(
            email,
            self.diligence_repository,
            self.grade_repository,
            request.json,
        )

        return HTTPResponse(status=204)


class ScoreGradeView(HTTPMethodView):
    @check_submit_status
    @ged_not_allowed
    def get(self, _: Request, email: str) -> HTTPResponse:
        ...

    @check_submit_status
    @ged_not_allowed
    def patch(self, _: Request, email: str) -> HTTPResponse:
        ...


class GedScoreGradeView(HTTPMethodView):
    @check_submit_status
    def get(self, _: Request, email: str) -> HTTPResponse:
        ...

    @check_submit_status
    def patch(self, _: Request, email: str) -> HTTPResponse:
        ...


bp_grade.add_route(DiligenceGradeView.as_view(), '/diligence')
bp_grade.add_route(ScoreGradeView.as_view(), '/score')
bp_grade.add_route(GedScoreGradeView.as_view(), '/ged-score')
