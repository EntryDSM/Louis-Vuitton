from sanic import Blueprint

from lv.presentation.classification import bp_classification
from lv.presentation.document import bp_document


# 모든 요청에 대해 에르스에다가 user_id 를 가지고 status - final_submit 이 false 인지를 검사하는 데코레이터
api = Blueprint.group(
    bp_classification,
    bp_document,
    url_prefix="/applicant/<email>",
)
