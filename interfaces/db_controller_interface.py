from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from model.eams_record import EAMSRecord


class BaseController(ABC):

    @abstractmethod
    def create(self, data: EAMSRecord):
        pass

    @abstractmethod
    def get(self, query: Dict[str, Any]) -> Optional[EAMSRecord]:
        pass

    @abstractmethod
    def list(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def update(self, query: Dict[str, Any], update_data: Dict[str, Any]) -> int:
        pass

    @abstractmethod
    def delete(self, query: Dict[str, Any]) -> int:
        pass
