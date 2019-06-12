from sqlalchemy import Column, ForeignKey, String, Table

from ..models import metadata


academic_information_tbl = Table(
    'academic_information',
    metadata,
    Column('applicant_email', String(320), primary_key=True),
    Column(
        'school_code',
        String(10),
        ForeignKey('school.code'),
        nullable=False
    ),
    Column('student_class', String(2)),
    Column('student_number', String(2)),
    Column('academic_tel', String(12)),
    Column('graduated_year', String(4)),

    Column('created_at', nullable=False),
    Column('updated_at', nullable=False),
)
