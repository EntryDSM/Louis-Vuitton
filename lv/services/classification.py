from typing import Any, Dict

from dacite.exceptions import MissingValueError, WrongTypeError

from lv.entities.classification import Classification
from lv.entities.helper import from_dict, to_dict
from lv.exceptions.service import (
    NotAllowedValueException,
    WrongClassificationDataException,
)
from lv.services.repository_interfaces.classification import (
    ClassificationRepositoryInterface
)


async def get_applicant_classification(
    email: str, repository: ClassificationRepositoryInterface
) -> Dict[str, Any]:
    classification: Classification = from_dict(
        data_class=Classification, data=await repository.get_one(email)
    )

    return to_dict(classification)


async def upsert_applicant_classification(
    email: str,
    repository: ClassificationRepositoryInterface,
    target: Dict[str, Any],
) -> None:
    try:
        classification = from_dict(data_class=Classification, data=target)
    except (NotAllowedValueException, MissingValueError, WrongTypeError):
        raise WrongClassificationDataException

    await repository.patch(email, to_dict(classification))
