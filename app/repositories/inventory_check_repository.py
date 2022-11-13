from app.repositories.mongo_repository import MongoRepository
from app.models.mongo.inventory_check import InventoryCheck
from datetime import datetime
from pymongo.collection import Collection


class InventoryCheckRepository(MongoRepository):

    def __init__(self) -> None:
        super().__init__()
        self.collection: Collection[InventoryCheck] = self.mongo_db.get_collection(
            'InventoryCheck')

    def get_last_check_stock_count(self, code: str) -> int:
        result = self.collection.find_one({"code": code})
        if (result is None):
            return 0
        return result['lastCheckStockCount']

    def update_inventory_check_count(self, code: str, item_count: int):

        self.collection.update_many(
            {
                "code": code,
            },
            {
                "$set": {
                    "lastCheckStockCount": item_count,
                    "lastCheckDateTime": datetime.now()
                }
            },
            upsert=True)
