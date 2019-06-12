import enum

from sqlalchemy import Column, Enum, String, Table
from sqlalchemy.dialects.mysql import INTEGER as Integer

from ..models import metadata


class SubjectChoice(enum.Enum):
    KOREAN = 1
    MATH = 2
    SOCIAL = 3
    SCIENCE = 4
    ENGLISH = 5
    HISTORY = 6
    TECH_HOME = 7


class ScoreChoice(enum.Enum):
    A = 1
    B = 2
    C = 3
    D = 4
    E = 5
    X = 6


grade_by_semester_tbl = Table(
    'grade_by_semester',
    metadata,
    Column('applicant_email', String(320), primary_key=True),
    Column('subject', Enum(SubjectChoice), primary_key=True),
    Column('semester', Integer(unsigned=True), primary_key=True),
    Column('score', Enum(ScoreChoice)),

    Column('created_at', nullable=False),
    Column('updated_at', nullable=False),
)
