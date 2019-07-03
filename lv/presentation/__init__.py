from sanic import Blueprint

from lv.presentation.classification import bp_classification
from lv.presentation.document import bp_document
from lv.presentation.record import bp_record


api = Blueprint.group(
    bp_classification,
    bp_document,
    bp_record,
    url_prefix="/applicant/<email>",
)
