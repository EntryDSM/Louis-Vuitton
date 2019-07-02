from typing import Any, Dict, Type

from lv.data.external_service.http import HTTPClient
from lv.exceptions.data import (
    ExternalServiceDownException,
    InterCallNotFoundException,
)
from lv.exceptions.service import (
    DataSourceFaultException,
    NonExistDataException,
)
from lv.services.repository_interfaces.applicant_status import (
    ApplicantStatusRepositoryInterface,
)

APPLICANT_STATUS_API_URL = '/applicant/{0}/status'


class ApplicantStatusRepository(ApplicantStatusRepositoryInterface):
    def __init__(self, host: str, client: Type[HTTPClient] = HTTPClient):
        self.client = client
        self.host = host + APPLICANT_STATUS_API_URL

    async def get_one(self, email: str) -> Dict[str, Any]:
        try:
            return await self.client.get(self.host.format(email))
        except ExternalServiceDownException:
            raise DataSourceFaultException
        except InterCallNotFoundException:
            raise NonExistDataException

    async def patch(self, email: str, target: Dict[str, Any]) -> None:
        ...
