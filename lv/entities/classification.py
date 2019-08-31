from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Classification:
    is_ged: bool
    apply_type: str
    social_detail_type: Optional[str]
    is_daejeon: bool
    is_graduated: Optional[bool]
    graduated_year: Optional[str]
    additional_type: Optional[str]
