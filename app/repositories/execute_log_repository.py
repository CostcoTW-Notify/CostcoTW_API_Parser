from app.repositories.mongo_repository import MongoRepository
from app.models.mongo.execute_log import ExecuteLogModel
from app.utility.datetime_helper import DateTimeHelper
from pymongo.collection import Collection
from typing import Optional


class ExecuteLogRepository(MongoRepository):

    def __init__(self) -> None:
        super().__init__()
        self.collection: Collection[ExecuteLogModel] = self.mongo_db.get_collection(
            "ExecuteLog")

    def check_today_already_execute(self, type: str) -> bool:
        today = DateTimeHelper.get_today_with_timezone()

        query: ExecuteLogModel = {
            "Type": type,
            "ExecuteDate": today
        }
        result = self.collection.count_documents(query)
        return result > 0

    def create_today_execute_log(self, type: str) -> bool:
        today = DateTimeHelper.get_today_with_timezone()
        log: ExecuteLogModel = {
            "Type": type,
            "ExecuteDate": today
        }
        result = self.collection.insert_one(dict(log))
        return result.acknowledged
