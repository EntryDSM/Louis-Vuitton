from sanic import Blueprint

from lv.presentation.classification import bp_classification
from lv.presentation.document import bp_document
from lv.presentation.grade import bp_grade


api = Blueprint.group(
    bp_classification,
    bp_document,
    bp_grade,
    url_prefix="/applicant/<email>",
)
