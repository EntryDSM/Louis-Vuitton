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
    INCOME_LEVEL_1 = 'income_level_1'
    INCOME_LEVEL_2 = 'income_level_2'
    INCOME_LEVEL_3 = 'income_level_3'
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
