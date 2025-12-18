from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from model.eams_record import EAMSRecord


class BaseCRUD(ABC):

    @abstractmethod
    def create(self, data: EAMSRecord) -> Any:
        pass

    @abstractmethod
    def get_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_many(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def update(self, query: Dict[str, Any], update_data: Dict[str, Any]) -> int:
        pass

    @abstractmethod
    def delete(self, query: Dict[str, Any]) -> int:
        pass
