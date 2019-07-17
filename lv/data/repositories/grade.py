from decimal import Decimal
from typing import Any, Dict, List, Type

from pypika import Parameter, Query

from lv.data.db.mysql import MySQLClient
from lv.data.db.tables import applicant_score_tbl, grade_by_semester_tbl
from lv.services.repository_interfaces.grade import (
    DiligenceGradeRepositoryInterface,
    GedGradeRepositoryInterface,
    GradeRepositoryInterface,
    ScoreGradeRepositoryInterface,
)


class DiligenceGradeRepository(DiligenceGradeRepositoryInterface):
    def __init__(self, db: Type[MySQLClient] = MySQLClient):
        self.db = db

    async def get_one(self, email: str) -> Dict[str, Any]:
        query: str = Query.from_(applicant_score_tbl).select(
            applicant_score_tbl.volunteer_time,
            applicant_score_tbl.full_cut_count,
            applicant_score_tbl.period_cut_count,
            applicant_score_tbl.late_count,
            applicant_score_tbl.early_leave_count
        ).where(
            applicant_score_tbl.applicant_email == Parameter("%s")
        ).get_sql(quote_char=None)

        return await self.db.fetchone(query, email)

    async def patch(self, email: str, target: Dict[str, Any]):
        query = Query.update(applicant_score_tbl).where(
            applicant_score_tbl.applicant_email == Parameter("%s")
        )

        for col in target:
            query = query.set(col, target[col])

        await self.db.execute(query.get_sql(quote_char=None), email)


class GradeRepository(GradeRepositoryInterface):
    def __init__(self, db: Type[MySQLClient] = MySQLClient):
        self.db = db

    async def patch(self, email: str, target: Dict[str, Any]):
        query = Query.update(applicant_score_tbl).where(
            applicant_score_tbl.applicant_email == Parameter("%s")
        )

        for col in target:
            query = query.set(col, target[col])

        await self.db.execute(query.get_sql(quote_char=None), email)


class SubjectScoreGradeRepository(ScoreGradeRepositoryInterface):
    def __init__(self, db: Type[MySQLClient] = MySQLClient):
        self.db = db

    async def get(self, email: str) -> List[Dict[str, Any]]:
        query: str = Query.from_(grade_by_semester_tbl).select(
            grade_by_semester_tbl.subject,
            grade_by_semester_tbl.semester,
            grade_by_semester_tbl.score
        ).where(
            applicant_score_tbl.applicant_email == Parameter("%s")
        ).get_sql(quote_char=None)

        return await self.db.fetchall(query, email)

    async def patch(self, email: str, target: Dict[str, Any]):
        ...


class GedGradeRepository(GedGradeRepositoryInterface):
    def __init__(self, db: Type[MySQLClient] = MySQLClient):
        self.db = db

    async def get_one(self, email: str) -> Dict[str, Any]:
        query: str = Query.from_(applicant_score_tbl).select(
            applicant_score_tbl.ged_average_score
        ).where(
            applicant_score_tbl.applicant_email == Parameter("%s")
        ).get_sql(quote_char=None)

        return await self.db.fetchone(query, email)

    async def patch(self, email: str, ged_average_score: Decimal):
        query = Query.update(applicant_score_tbl).set(
            applicant_score_tbl.ged_average_score, ged_average_score
        ).where(
            applicant_score_tbl.applicant_email == Parameter("%s")
        ).get_sql(quote_char=None)

        await self.db.execute(query, email)
