import pymongo
from typing import Dict, Any, Optional, List
from pymongo import MongoClient

from constants.mongo_db_configs import MONGO_DB_URL, MONGO_DB_NAME, MONGO_DB_COLLECTION, MONGO_DB_PK
from enums.eams_status import EAMSStatus
from enums.iecc_console import IECCConsole
from interfaces.db_manager_interface import BaseCRUD
from model.eams_record import EAMSRecord


class MongoCRUD(BaseCRUD):
    def __init__(self, uri: str, db_name: str, collection_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        self.collection.create_index(MONGO_DB_PK, unique=True)

    def create(self, data: EAMSRecord) -> str:
        d = data.to_dict()
        result = self.collection.insert_one(d)
        return str(result.inserted_id)

    def get_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return self.collection.find_one(query)

    def get_many(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        return list(self.collection.find(query))

    def update(self, query: Dict[str, Any], update_data: Dict[str, Any]) -> int:
        result = self.collection.update_one(query, {"$set": update_data}, upsert=True)
        return result.modified_count

    def delete(self, query: Dict[str, Any]) -> int:
        result = self.collection.delete_one(query)
        return result.deleted_count


if __name__ == "__main__":
    db_client = MongoCRUD(
        MONGO_DB_URL,
        MONGO_DB_NAME,
        MONGO_DB_COLLECTION
    )
    sample_record = EAMSRecord(
        123,
        202501,
        IECCConsole.DUAT,
        EAMSStatus.OPENED,
        ""
    )
    # db_client.create(sample_record)
    print("done")
    r = db_client.get_one({"eams_wo": 456})
    eams_r = EAMSRecord(**r)
    print(f"obtained result: {r}")
    # url = r"mongodb+srv://camfurt_db_user:RDTYmfKDHRZp6Smp@cluster0.cmoqi6n.mongodb.net/?appName=Cluster0"
    # client = pymongo.MongoClient(url)
    # names = client.list_database_names()
    # print(f"{names=}")

    # create a new database
    # db = client["my_new_database"]
    # create a collection
    # users = db["users"]
    # create a record to initiate the creation of the database
    # users.insert_one({
    #     "name": "Alice",
    #     "age": 30,
    #     "role": "admin"
    # })

    # update a record
    # users.
