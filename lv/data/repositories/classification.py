from typing import Any, Dict, Type

from pypika import Parameter, Query

from lv.data.db.mysql import MySQLClient
from lv.data.db.tables import classification_tbl
from lv.services.repository_interfaces.classification import (
    ClassificationRepositoryInterface
)


class ClassificationRepository(ClassificationRepositoryInterface):
    def __init__(self, db: Type[MySQLClient] = MySQLClient):
        self.db = db

    async def get_one(self, email: str) -> Dict[str, Any]:
        query: str = Query.from_(classification_tbl).select(
            classification_tbl.applicant_email,
            classification_tbl.apply_type,
            classification_tbl.is_ged,
            classification_tbl.is_daejeon,
            classification_tbl.is_graduated,
            classification_tbl.additional_type,
            classification_tbl.social_detail_type,
            classification_tbl.graduated_year
        ).where(
            classification_tbl.applicant_email == Parameter("%s")
        ).get_sql(quote_char=None)

        return await self.db.fetchone(query, email)

    async def patch(self, email: str, target: Dict[str, Any]) -> None:
        query = Query.update(classification_tbl).where(
            classification_tbl.applicant_email == Parameter("%s")
        )

        for col in target:
            query = query.set(col, target[col])

        await self.db.execute(query.get_sql(quote_char=None), email)
