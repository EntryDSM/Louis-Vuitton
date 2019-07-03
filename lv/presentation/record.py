from sanic import Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse
from sanic.views import HTTPMethodView

from lv.presentation.helper import check_submit_status

bp_record = Blueprint("record", url_prefix="/record")


class VolunteerAndAttendanceRecordView(HTTPMethodView):
    @check_submit_status
    def get(self, _: Request, email: str) -> HTTPResponse:
        ...

    @check_submit_status
    def patch(self, _: Request, email: str) -> HTTPResponse:
        ...


class ScoreRecordView(HTTPMethodView):
    @check_submit_status
    def get(self, _: Request, email: str) -> HTTPResponse:
        ...

    @check_submit_status
    def patch(self, _: Request, email: str) -> HTTPResponse:
        ...


class GedScoreRecordView(HTTPMethodView):
    @check_submit_status
    def get(self, _: Request, email: str) -> HTTPResponse:
        ...

    @check_submit_status
    def patch(self, _: Request, email: str) -> HTTPResponse:
        ...


bp_record.add_route(
    VolunteerAndAttendanceRecordView.as_view(), '/volunteer-attendance'
)
bp_record.add_route(ScoreRecordView.as_view(), '/score')
bp_record.add_route(GedScoreRecordView.as_view(), '/ged-score')
