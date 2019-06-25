from typing import Any, Dict

from dacite import MissingValueError, WrongTypeError

from lv.entities.document import AttachedDocument
from lv.entities.helper import from_dict, to_dict
from lv.exceptions.service import WrongDocumentDataException
from lv.services.repository_interfaces.document import (
    AttachedDocumentRepositoryInterface
)


async def get_attached_documents(
    email: str, repository: AttachedDocumentRepositoryInterface
) -> Dict[str, Any]:
    documents: AttachedDocument = from_dict(
        data_class=AttachedDocument, data=await repository.get_one(email)
    )

    return to_dict(documents)


async def upsert_attached_documents(
    email: str,
    repository: AttachedDocumentRepositoryInterface,
    target: Dict[str, Any],
):
    try:
        documents = from_dict(data_class=AttachedDocument, data=target)
    except (MissingValueError, WrongTypeError):
        raise WrongDocumentDataException

    await repository.patch(email, to_dict(documents))
