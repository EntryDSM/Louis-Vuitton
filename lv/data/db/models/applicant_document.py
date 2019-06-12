from sqlalchemy import Column, String, Table, Text

from ..models import metadata


applicant_document_tbl = Table(
    'applicant_document',
    metadata,
    Column('applicant_email', String(320), primary_key=True),
    Column('self_introduction_text', Text),
    Column('study_plan_text', Text),

    Column('created_at', nullable=False),
    Column('updated_at', nullable=False),
)
