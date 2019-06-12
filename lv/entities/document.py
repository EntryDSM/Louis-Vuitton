from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class AttachedDocument:
    self_introduction_text: Optional[str]
    study_plan_text: Optional[str]
