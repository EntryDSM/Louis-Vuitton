from functools import wraps

from sanic.request import Request
from sanic.response import HTTPResponse

from lv.data.repositories.applicant_status import ApplicantStatusRepository
from lv.data.repositories.classification import ClassificationRepository
from lv.exceptions.http import (
    Forbidden,
    InternalServerError,
    NotFoundApplicant,
)
from lv.exceptions.service import (
    DataSourceFailureException,
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
        except DataSourceFailureException:
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


def check_is_ged(allow: bool=False):
    def outer_function(original_function):
        @wraps(original_function)
        async def decorated_function(request: Request, *args, **kwargs):
            repository = ClassificationRepository()

            classification = await repository.get_one(kwargs['email'])

            if classification['is_ged'] is allow:
                response: HTTPResponse = await original_function(
                    request, *args, **kwargs
                )

                return response

            raise Forbidden('Ged not allowed')
        return decorated_function
    return outer_function
