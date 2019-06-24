from abc import ABC, abstractmethod
from typing import Any, Dict


class AttachedDocumentRepositoryInterface(ABC):
    @abstractmethod
    async def get_one(self, email: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def patch(self, email: str, target: Dict[str, Any]) -> None:
        pass
