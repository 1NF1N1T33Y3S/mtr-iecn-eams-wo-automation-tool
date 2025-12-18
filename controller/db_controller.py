from typing import Any, Dict, List, Optional

from pymongo.errors import DuplicateKeyError

from constants.mongo_db_configs import MONGO_DB_PK
from helper.logging_helper import logger
from interfaces.db_controller_interface import BaseController
from interfaces.db_manager_interface import BaseCRUD
from model.eams_record import EAMSRecord


class GenericController(BaseController):
    def __init__(self, crud: BaseCRUD):
        self.crud = crud

    def create(self, data: EAMSRecord):
        # business logic could go here
        return self.crud.create(data)

    def get(self, by_eams_wo: int) -> Optional[EAMSRecord]:
        query = {MONGO_DB_PK: by_eams_wo}
        r = self.crud.get_one(query)
        if r is None:
            return None
        return EAMSRecord(**r)

    def list(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        return self.crud.get_many(query)

    def update(self, by_eams_wo: int, update_data: Dict[str, Any]) -> int:
        query = {MONGO_DB_PK: by_eams_wo}
        logger.info(f"updating to db {query=} {update_data=}")
        return self.crud.update(query, update_data)

    def delete(self, query: Dict[str, Any]) -> int:
        return self.crud.delete(query)
