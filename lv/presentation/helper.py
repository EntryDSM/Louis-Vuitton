from functools import wraps

from sanic.request import Request
from sanic.response import HTTPResponse

from lv.data.repositories.applicant_status import ApplicantStatusRepository
from lv.exceptions.http import (
    Forbidden,
    InternalServerError,
    NotFoundApplicant,
)
from lv.exceptions.service import (
    DataSourceFaultException,
    NonExistDataException,
)


def check_submit_status(original_function):
    @wraps(original_function)
    async def decorated_function(request: Request, *args, **kwargs):
        repository = ApplicantStatusRepository(
            request.app.config['HERMES_HOST']
        )

        try:
            applicant_status = await repository.get_one(kwargs['email'])
        except DataSourceFaultException:
            raise InternalServerError('Data source fault')
        except NonExistDataException:
            raise NotFoundApplicant("Not found applicant")

        is_final_submit: bool = applicant_status['is_final_submit']

        if is_final_submit:
            response: HTTPResponse = await original_function(
                request, *args, **kwargs
            )
            return response

        raise Forbidden('Already submitted applicant')

    return decorated_function
