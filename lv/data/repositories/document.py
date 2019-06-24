from typing import Any, Dict, Type

from pypika import Parameter, Query

from lv.data.db.mysql import MySQLClient
from lv.data.db.tables import attached_document_tbl
from lv.services.repository_interfaces.document import (
    AttachedDocumentRepositoryInterface
)


class AttachedDocumentRepository(AttachedDocumentRepositoryInterface):
    def __init__(self, db: Type[MySQLClient] = MySQLClient):
        self.db = db

    async def get_one(self, email: str) -> Dict[str, Any]:
        query: str = Query.from_(attached_document_tbl).select(
            attached_document_tbl.self_introduction_text,
            attached_document_tbl.study_plan_text
        ).where(
            attached_document_tbl.applicant_email == Parameter("%s")
        ).get_sql(quote_char=None)

        return await self.db.fetchone(query, email)

    async def patch(self, email: str, target: Dict[str, Any]):
        query = Query.update(attached_document_tbl).where(
            attached_document_tbl.applicant_email == Parameter("%s")
        )

        for col in target:
            query = query.set(col, target[col])

        await self.db.execute(query.get_sql(quote_char=None), email)
