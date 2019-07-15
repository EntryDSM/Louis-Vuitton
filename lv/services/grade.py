from decimal import Decimal
from typing import Any, Dict

from dacite import MissingValueError, WrongTypeError

from lv.entities.grade import DiligenceGrade, Grade
from lv.entities.helper import from_dict, to_dict
from lv.exceptions.service import WrongDiligenceGradeDataException
from lv.services.repository_interfaces.grade import (
    DiligenceGradeRepositoryInterface,
    GradeRepositoryInterface,
)

ATTENDANCE_SCORE_MAXIMUM = 15


async def get_diligence_grade(
    email: str, repository: DiligenceGradeRepositoryInterface
) -> Dict[str, Any]:
    diligence_grade: DiligenceGrade = from_dict(
        data_class=DiligenceGrade, data=await repository.get_one(email)
    )

    return to_dict(diligence_grade)


async def _patch_diligence_grade(
    email: str,
    repository: DiligenceGradeRepositoryInterface,
    target: Dict[str, Any],
) -> DiligenceGrade:
    try:
        diligence_grade = from_dict(data_class=DiligenceGrade, data=target)
    except (MissingValueError, WrongTypeError):
        raise WrongDiligenceGradeDataException

    await repository.patch(email, to_dict(diligence_grade))

    return from_dict(
        data_class=DiligenceGrade, data=await repository.get_one(email)
    )


async def _calculate_attendance_score(diligence_grade: DiligenceGrade) -> int:
    d = diligence_grade

    conversion_absence_days: int = (
        d.period_cut_count + d.late_count + d.early_leave_count
    ) // 3
    total_absence_days: int = d.full_cut_count + conversion_absence_days

    if total_absence_days >= 15:
        attendance_score = 0
    else:
        attendance_score = ATTENDANCE_SCORE_MAXIMUM - total_absence_days

    return attendance_score


async def _calculate_volunteer_score(
    diligence_grade: DiligenceGrade
) -> Decimal:
    volunteer_time = diligence_grade.volunteer_time

    if volunteer_time >= 50:
        volunteer_score = Decimal('15')
    elif 15 <= volunteer_time <= 49:
        volunteer_score = round(
            Decimal(str((volunteer_time - 14) / 3)) + 3, 3
        )
    else:
        volunteer_score = Decimal('3')

    return volunteer_score


async def upsert_diligence_grade(
    email: str,
    diligence_repository: DiligenceGradeRepositoryInterface,
    grade_repository: GradeRepositoryInterface,
    target: Dict[str, Any],
):
    diligence_grade = await _patch_diligence_grade(
        email, diligence_repository, target
    )

    attendance_score: int = await _calculate_attendance_score(diligence_grade)
    volunteer_score: Decimal = await _calculate_volunteer_score(
        diligence_grade
    )

    grade = from_dict(data_class=Grade, data={
        'attendance_score': attendance_score,
        'volunteer_score': volunteer_score
    })

    await grade_repository.patch(email, to_dict(grade))
