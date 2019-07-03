from sanic import Blueprint

from lv.presentation.classification import bp_classification
from lv.presentation.document import bp_document


api = Blueprint.group(
    bp_classification,
    bp_document,
    url_prefix="/applicant/<email>",
)
