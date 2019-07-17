from abc import ABC, abstractmethod
from typing import Any, Dict


class ApplicantStatusRepositoryInterface(ABC):
    @abstractmethod
    async def get_one(self, email: str) -> Dict[str, Any]:
        pass
