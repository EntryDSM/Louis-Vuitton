from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Any, Dict, List


class DiligenceGradeRepositoryInterface(ABC):
    @abstractmethod
    async def get_one(self, email: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def patch(self, email: str, target: Dict[str, Any]) -> None:
        pass


class GradeRepositoryInterface(ABC):
    @abstractmethod
    async def patch(self, email: str, target: Dict[str, Any]) -> None:
        pass


class ScoreGradeRepositoryInterface(ABC):
    @abstractmethod
    async def get(self, email: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def patch(self, email: str, target: Dict[str, Any]) -> None:
        pass


class GedGradeRepositoryInterface(ABC):
    @abstractmethod
    async def get_one(self, email: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def patch(self, email: str, ged_average_score: Decimal) -> None:
        pass
