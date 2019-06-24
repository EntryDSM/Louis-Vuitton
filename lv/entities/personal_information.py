from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class School:
    school_code: str
    school_name: str
    school_full_name: str
    education_office: str


@dataclass(frozen=True)
class PersonalInformation:
    school: Optional[School]
    academic_tel: Optional[str]
