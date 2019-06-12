from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ApplyType(Enum):
    COMMON = 'common'
    MEISTER = 'meister'
    SOCIAL = 'social'


class SocialDetailType(Enum):
    ONE_PARENT = 'one_parent'
    FROM_NORTH = 'from_north'
    MULTICULTURAL_FAMILY = 'multicultural_family'
    INCOME_LEVEL_BASE = 'income_level_base'
    INCOME_LEVEL_SECOND = 'income_level_second'
    INCOME_LEVEL_THIRD = 'income_level_third'
    ETC = 'etc'


class AdditionalType(Enum):
    NATIONAL_MERIT = 'national_merit'
    SPECIAL_ADMISSION = 'special_admission'


@dataclass(frozen=True)
class Classification:
    is_ged: bool
    apply_type: ApplyType
    social_detail_type: Optional[SocialDetailType]
    is_daejeon: bool
    is_graduated: Optional[bool]
    graduated_year: Optional[int]
    additional_type: Optional[AdditionalType]
