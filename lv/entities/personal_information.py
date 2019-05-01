from enum import Enum
from dataclasses import dataclass

from typing import Optional


class Sex(Enum):
    MALE = 'male'
    FEMALE = 'female'


@dataclass(frozen=True)
class School:
    school_code: str
    school_name: str
    school_full_name: str
    education_office: str


@dataclass(frozen=True)
class PersonalInformation:
    applicant_name: Optional[str]
    sex: Sex
    birth_date: Optional[str]
    school: Optional[School]
    student_class: str
    student_number: str
    parent_name: Optional[str]
    academic_tel: Optional[str]
    parent_tel: Optional[str]
    applicant_tel: Optional[str]
    address: Optional[str]
    post_code: Optional[str]
    image_path: Optional[str]
