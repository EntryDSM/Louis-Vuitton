from sqlalchemy import Boolean, Column, String, Table
from sqlalchemy.dialects.mysql import INTEGER as Integer

from ..models import metadata


applicant_status = Table(
    'applicant_status',
    metadata,
    Column('applicant_email', String(320), primary_key=True),
    Column(
        'receipt_code',
        Integer(display_width=3, zerofill=True, unsigned=True),
        unique=True,
        autoincrement=True,
        nullable=False,
    ),
    Column('is_paid', Boolean, nullable=False, default=False),
    Column(
        'is_printed_application_arrived',
        Boolean,
        nullable=False,
        default=False
    ),
    Column('is_passed_first_apply', Boolean, nullable=False, default=False),
    Column('is_final_submit', Boolean, nullable=False, default=False),
    Column('exam_code', String(6), unique=True),

    Column('created_at', nullable=False),
    Column('updated_at', nullable=False),
)
