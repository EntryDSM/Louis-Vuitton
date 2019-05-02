from enum import Enum
from dataclasses import dataclass
from typing import Optional, List


class ScoreType(Enum):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'
    X = 'X'


@dataclass(frozen=True)
class SubjectScore:
    korean: ScoreType
    math: ScoreType
    social: ScoreType
    science: ScoreType
    english: ScoreType
    history: ScoreType
    tech_home: ScoreType


@dataclass(frozen=True)
class Grade:
    volunteer_time: Optional[int]
    full_cut_count: Optional[int]
    period_cut_count: Optional[int]
    late_count: Optional[int]
    early_leave_count: Optional[int]

    ged_average_score: Optional[float]
    subject_score: Optional[List[SubjectScore]]

    volunteer_score: Optional[int]
    attendance_score: Optional[int]
    conversion_score: Optional[float]
    final_score: Optional[float]



