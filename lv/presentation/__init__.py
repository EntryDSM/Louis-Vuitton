from sanic import Blueprint

from .classification import bp_classification


# 모든 요청에 대해 에르스에다가 user_id 를 가지고 status - final_submit 이 false 인지를 검사하는 데코레이터
api = Blueprint.group(bp_classification, url_prefix="/applicant/<user_id>")
