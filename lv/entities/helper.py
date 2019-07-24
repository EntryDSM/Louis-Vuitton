from dataclasses import asdict
from decimal import Decimal
from typing import Any, Dict, List, Type, TypeVar, Optional

import dacite

from lv.entities.classification import Classification
from lv.entities.grade import AcademicGrade
from lv.entities.constant import (
    ALLOWABLE_ADDITIONAL_TYPES,
    ALLOWABLE_APPLY_TYPES,
    ALLOWABLE_GRADUATED_SEMESTER_RANGE,
    ALLOWABLE_SCORE_TYPES,
    ALLOWABLE_SUBJECT_TYPES,
    ALLOWABLE_SOCIAL_DETAIL_TYPES,
    ALLOWABLE_UNDERGRADUATE_SEMESTER_RANGE,
)
from lv.exceptions.service import NotAllowedValueException

T = TypeVar("T")


def to_dict(entity_instance: T) -> Dict[str, Any]:
    return {k: v for k, v in asdict(entity_instance).items() if v is not None}


def from_dict(
    data_class: Type[T],
    data: Dict[str, Any],
    decimal_auto_convert: bool = False,
) -> T:
    if decimal_auto_convert:
        data = {
            k: Decimal(str(v)) for k, v in data.items() if isinstance(float, v)
        }

    entity: T = dacite.from_dict(data_class=data_class, data=data)

    if isinstance(entity, Classification):
        _validate_classification_data(entity)
    elif isinstance(entity, AcademicGrade) and entity.subject_scores:
        _validate_academic_grade_data(entity)

    return entity


def _enum_validate(
    target: Optional[str], allowable_list: List[str], nullable: bool = False
) -> bool:
    if target is None:
        return nullable

    return target in allowable_list


def _integer_range_validate(
    target: int, allowable_range: range
) -> bool:
    return target in allowable_range


def _validate_classification_data(entity: Classification) -> None:
    is_allowed_apply_type = _enum_validate(
        entity.apply_type, ALLOWABLE_APPLY_TYPES
    )
    is_allowed_social_detail_type = _enum_validate(
        entity.social_detail_type, ALLOWABLE_SOCIAL_DETAIL_TYPES, nullable=True
    )
    is_allowed_additional_type = _enum_validate(
        entity.additional_type, ALLOWABLE_ADDITIONAL_TYPES, nullable=True
    )

    if not (
        is_allowed_apply_type
        and
        is_allowed_social_detail_type
        and
        is_allowed_additional_type
    ):
        raise NotAllowedValueException


def _get_allowable_range(scores_len: int) -> range:
    if scores_len == len(ALLOWABLE_GRADUATED_SEMESTER_RANGE):
        return ALLOWABLE_GRADUATED_SEMESTER_RANGE
    elif scores_len == len(ALLOWABLE_UNDERGRADUATE_SEMESTER_RANGE):
        return ALLOWABLE_UNDERGRADUATE_SEMESTER_RANGE
    else:
        raise NotAllowedValueException


def _validate_academic_grade_data(
    entity: AcademicGrade
) -> None:
    scores = entity.subject_scores

    for score in scores:
        if not _enum_validate(score.score, ALLOWABLE_SCORE_TYPES):
            raise NotAllowedValueException
        if not _enum_validate(score.subject, ALLOWABLE_SUBJECT_TYPES):
            raise NotAllowedValueException
        if not _integer_range_validate(
            score.semester, _get_allowable_range(len(scores))
        ):
            raise NotAllowedValueException
