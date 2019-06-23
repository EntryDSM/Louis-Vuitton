from typing import Any, Dict, List, Type, TypeVar
from dataclasses import asdict

import dacite
from dacite.exceptions import DaciteFieldError

from lv.entities.classification import Classification
from lv.entities.grade import ScoreGrade
from lv.entities.constant import (
    ALLOWABLE_ADDITIONAL_TYPES,
    ALLOWABLE_APPLY_TYPES,
    ALLOWABLE_SCORE_TYPES,
    ALLOWABLE_SOCIAL_DETAIL_TYPES,
)

T = TypeVar("T")


def to_dict(entity_instance: T) -> Dict[str, Any]:
    return {k: v for k, v in asdict(entity_instance).items() if v is not None}


def from_dict(data_class: Type[T], data: Dict[str, Any]) -> T:
    entity: T = dacite.from_dict(data_class=data_class, data=data)

    if isinstance(entity, Classification):
        _classification_from_dict(entity)
    elif isinstance(entity, ScoreGrade) and entity.subject_score:
        _score_grade_from_dict(entity)

    return entity


def _enum_validate(target: str, allowable_list: List[str]) -> bool:
    return target in allowable_list


def _classification_from_dict(entity: Classification) -> None:
    is_allowed_apply_type = _enum_validate(
        entity.apply_type, ALLOWABLE_APPLY_TYPES
    )
    is_allowed_social_detail_type = _enum_validate(
        entity.social_detail_type, ALLOWABLE_SOCIAL_DETAIL_TYPES.append(None)
    )
    is_allowed_additional_type = _enum_validate(
        entity.additional_type, ALLOWABLE_ADDITIONAL_TYPES.append(None)
    )

    if not (
        is_allowed_apply_type
        and
        is_allowed_social_detail_type
        and
        is_allowed_additional_type
    ):
        raise DaciteFieldError


def _score_grade_from_dict(entity: ScoreGrade) -> None:
    for subject in entity.subject_score:
        for score in asdict(subject).values():
            if _enum_validate(score, ALLOWABLE_SCORE_TYPES):
                raise DaciteFieldError
