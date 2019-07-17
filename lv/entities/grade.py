from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, List


@dataclass(frozen=True)
class SubjectScore:
    korean: str
    math: str
    social: str
    science: str
    english: str
    history: str
    tech_home: str


@dataclass(frozen=True)
class Grade:
    volunteer_score: Optional[Decimal]
    attendance_score: Optional[int]
    conversion_score: Optional[Decimal]
    final_score: Optional[Decimal]


@dataclass(frozen=True)
class SubjectScoreGrade:
    subject_score: Optional[List[SubjectScore]]


@dataclass(frozen=True)
class GedGrade:
    ged_average_score: Optional[Decimal]


@dataclass(frozen=True)
class DiligenceGrade:
    volunteer_time: Optional[int]
    full_cut_count: Optional[int]
    period_cut_count: Optional[int]
    late_count: Optional[int]
    early_leave_count: Optional[int]
