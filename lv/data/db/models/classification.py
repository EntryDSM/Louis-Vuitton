import enum

from sqlalchemy import Boolean, Column, Enum, String, Table

from ..models import metadata


class ApplyTypeChoice(enum.Enum):
    COMMON = 1
    MEISTER = 2
    SOCIAL = 3


class AdditionalTypeChoice(enum.Enum):
    NATIONAL_MERIT = 1
    SPECIAL_ADMISSION = 2


class SocialDetailTypeChoice(enum.Enum):
    ONE_PARENT = 1
    FROM_NORTH = 2
    MULTICULTURAL_FAMILY = 3
    INCOME_LEVEL_1 = 4
    INCOME_LEVEL_2 = 5
    INCOME_LEVEL_3 = 6
    ETC = 7


classification = Table(
    'classification',
    metadata,
    Column('applicant_email', String(320), primary_key=True),
    Column('apply_type', Enum(ApplyTypeChoice)),
    Column('is_ged', Boolean),
    Column('is_daejeon', Boolean),
    Column('is_graduated', Boolean),
    Column('additional_type', Enum(AdditionalTypeChoice)),
    Column('social_detail_type', Enum(SocialDetailTypeChoice)),

    Column('created_at', nullable=False),
    Column('updated_at', nullable=False),
)
