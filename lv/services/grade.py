from decimal import Decimal
from typing import Any, Dict

from dacite import MissingValueError, WrongTypeError

from lv.entities.constant import ALLOWABLE_APPLY_TYPES
from lv.entities.grade import DiligenceGrade, GedGrade, Grade
from lv.entities.helper import from_dict, to_dict
from lv.exceptions.service import (
    WrongDiligenceGradeDataException,
    WrongGedGradeDataException,
)
from lv.services.classification import get_applicant_classification
from lv.services.repository_interfaces.classification import (
    ClassificationRepositoryInterface,
)
from lv.services.repository_interfaces.grade import (
    DiligenceGradeRepositoryInterface,
    GedGradeRepositoryInterface,
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
    elif 49 >= volunteer_time >= 15:
        volunteer_score = round(
            Decimal(str(volunteer_time - 14)) / 36 * 12 + 3, 3
        )
    else:
        volunteer_score = Decimal('3')

    return volunteer_score


async def _update_diligence_score_grade(
    diligence_grade: DiligenceGrade,
    repository: GradeRepositoryInterface,
    email: str,
):
    attendance_score: int = await _calculate_attendance_score(diligence_grade)
    volunteer_score: Decimal = await _calculate_volunteer_score(
        diligence_grade
    )

    grade = from_dict(data_class=Grade, data={
        'attendance_score': attendance_score,
        'volunteer_score': volunteer_score
    })

    await repository.patch(email, to_dict(grade))


async def upsert_diligence_grade(
    email: str,
    diligence_repository: DiligenceGradeRepositoryInterface,
    grade_repository: GradeRepositoryInterface,
    target: Dict[str, Any],
) -> None:
    diligence_grade = await _patch_diligence_grade(
        email, diligence_repository, target
    )

    await _update_diligence_score_grade(
        diligence_grade, grade_repository, email
    )


async def get_ged_grade(
    email: str, repository: GedGradeRepositoryInterface
) -> Dict[str, Any]:
    ged_grade: GedGrade = from_dict(
        data_class=GedGrade, data=await repository.get_one(email)
    )

    return to_dict(ged_grade)


async def _patch_ged_grade(
    email: str,
    repository: GedGradeRepositoryInterface,
    target: Dict[str, Any]
) -> GedGrade:
    try:
        ged_grade = from_dict(data_class=GedGrade, data=target)
    except (MissingValueError, WrongTypeError):
        raise WrongGedGradeDataException

    await repository.patch(email, ged_grade.ged_average_score)

    return from_dict(
        data_class=GedGrade, data=await repository.get_one(email)
    )


async def _update_ged_applicant_grade(
    ged_grade: GedGrade,
    grade_repository: GradeRepositoryInterface,
    classification_repository: ClassificationRepositoryInterface,
    email: str
):
    classification: str = await _get_classification_for_grade_calculation(
        email, classification_repository
    )

    attendance_score: int = ATTENDANCE_SCORE_MAXIMUM
    volunteer_score: Decimal = await _calculate_ged_volunteer_score(ged_grade)
    conversion_score: Decimal = await _calculate_ged_conversion_score(
        ged_grade,
        classification.lower(),
    )
    final_score: Decimal = (
        attendance_score + volunteer_score + conversion_score
    )

    grade = from_dict(data_class=Grade, data={
        'attendance_score': attendance_score,
        'volunteer_score': volunteer_score,
        'conversion_score': conversion_score,
        'final_score': final_score,
    })

    await grade_repository.patch(email, to_dict(grade))


async def _calculate_ged_volunteer_score(ged_grade: GedGrade) -> Decimal:
    ged_average_score: Decimal = ged_grade.ged_average_score

    return round((ged_average_score - 40) / 60 * 12 + 3, 3)


async def _calculate_ged_conversion_score(
    ged_grade: GedGrade, classification: str
) -> Decimal:
    ged_average_score: Decimal = ged_grade.ged_average_score

    if classification == ALLOWABLE_APPLY_TYPES[0]:
        conversion_score = round((ged_average_score - 50) / 50 * 150, 3)
    else:
        conversion_score = round((ged_average_score - 50) / 50 * 90, 3)

    return conversion_score


async def _get_classification_for_grade_calculation(
    email,
    repository: ClassificationRepositoryInterface
) -> str:
    classification = await get_applicant_classification(
        email, repository
    )

    return classification['apply_type']


async def upsert_ged_applicant_grade(
    email: str,
    ged_repository: GedGradeRepositoryInterface,
    grade_repository: GradeRepositoryInterface,
    classification_repository: ClassificationRepositoryInterface,
    target: Dict[str, Any],
) -> None:
    ged_grade = await _patch_ged_grade(
        email, ged_repository, target
    )

    await _update_ged_applicant_grade(
        ged_grade, grade_repository, classification_repository, email
    )
