from sqlalchemy import Column, Table, String

from ..models import metadata


school = Table(
    'school',
    metadata,
    Column('code', String(10), primary_key=True),
    Column('school_name', String(50)),
    Column('school_full_name', String(60)),
    Column('education_office', String(20)),
)
