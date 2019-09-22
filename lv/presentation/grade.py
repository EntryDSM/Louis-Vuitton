from sanic import Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView

from lv.exceptions.http import BadRequestParameter
from lv.exceptions.service import (
    WrongDiligenceGradeDataException,
    WrongGedGradeDataException,
)
from lv.data.repositories.classification import ClassificationRepository
from lv.data.repositories.grade import (
    AcademicGradeRepository,
    DiligenceGradeRepository,
    GedGradeRepository,
    GradeRepository,
)
from lv.presentation.helper import (
    check_is_ged,
    check_submit_status,
)
from lv.services.grade import (
    get_academic_grade,
    get_diligence_grade,
    get_ged_grade,
    upsert_academic_grade,
    upsert_diligence_grade,
    upsert_ged_applicant_grade,
)

bp_grade = Blueprint("grade", url_prefix="/grade")


class DiligenceGradeView(HTTPMethodView):
    diligence_repository = DiligenceGradeRepository()
    grade_repository = GradeRepository()

    @check_submit_status
    @check_is_ged(allow=False)
    def get(self, _: Request, email: str) -> HTTPResponse:
        diligence_grade = await get_diligence_grade(
            email, self.diligence_repository
        )

        return json(status=200, body=diligence_grade)

    @check_submit_status
    @check_is_ged(allow=False)
    def patch(self, request: Request, email: str) -> HTTPResponse:
        try:
            await upsert_diligence_grade(
                email,
                self.diligence_repository,
                self.grade_repository,
                request.json,
            )
        except WrongDiligenceGradeDataException:
            raise BadRequestParameter('Invalid diligence grade value')

        return HTTPResponse(status=204)


class AcademicGradeView(HTTPMethodView):
    academic_repository = AcademicGradeRepository()
    grade_repository = GradeRepository()
    classification_repository = ClassificationRepository()

    @check_submit_status
    @check_is_ged(allow=False)
    def get(self, _: Request, email: str) -> HTTPResponse:
        academic_grade = await get_academic_grade(
            email, self.academic_repository
        )

        return json(
            status=200, body=academic_grade
        )

    @check_submit_status
    @check_is_ged(allow=False)
    def patch(self, request: Request, email: str) -> HTTPResponse:
        await upsert_academic_grade(
            email,
            self.academic_repository,
            self.grade_repository,
            self.classification_repository,
            request.json
        )

        return HTTPResponse(status=204)


class GedScoreGradeView(HTTPMethodView):
    ged_repository = GedGradeRepository()
    grade_repository = GradeRepository()
    classification_repository = ClassificationRepository()

    @check_submit_status
    @check_is_ged(allow=True)
    def get(self, _: Request, email: str) -> HTTPResponse:
        ged_grade = await get_ged_grade(email, self.ged_repository)

        return json(status=200, body=ged_grade)

    @check_submit_status
    @check_is_ged(allow=True)
    def patch(self, request: Request, email: str) -> HTTPResponse:
        try:
            await upsert_ged_applicant_grade(
                email,
                self.ged_repository,
                self.grade_repository,
                self.classification_repository,
                request.json
            )
        except WrongGedGradeDataException:
            raise BadRequestParameter('Invalid ged grade value')

        return HTTPResponse(status=204)


bp_grade.add_route(DiligenceGradeView.as_view(), '/diligence')
bp_grade.add_route(AcademicGradeView.as_view(), '/academic-score')
bp_grade.add_route(GedScoreGradeView.as_view(), '/ged-score')
