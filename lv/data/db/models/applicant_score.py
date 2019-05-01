from sqlalchemy import Column, String, Table, Integer
from sqlalchemy.dialects.mysql import DOUBLE as Double

from ..models import metadata


applicant_score = Table(
    'applicant_score',
    metadata,
    Column('applicant_email', String(320), primary_key=True),
    Column('volunteer_time', Integer),
    Column('full_cut_count', Integer),
    Column('period_cut_count', Integer),
    Column('late_count', Integer),
    Column('early_leave_count', Integer),
    Column('volunteer_score', Integer),
    Column('attendance_score', Integer),
    Column('conversion_score', Double(unsigned=True)),
    Column('ged_average_score', Double(unsigned=True)),
    Column('final_score', Double(unsigned=True)),

    Column('created_at', nullable=False),
    Column('updated_at', nullable=False),
)
