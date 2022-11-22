from app.repositories.mongo_repository import MongoRepository, MongoClient
from app.models.mongo.server_log import ServerLog
from pymongo.collection import Collection


class ServerLogRepository(MongoRepository):

    def __init__(self, client: MongoClient) -> None:
        super().__init__(client)
        self.collection: Collection[ServerLog] = self.mongo_db.get_collection(
            'ServerLog')

    def insert_log(self, log: ServerLog) -> None:

        self.collection.insert_one(dict(log))
        pass
