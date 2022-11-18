import abc
from pymongo import MongoClient


class MongoRepository(abc.ABC):

    def __init__(self, client: MongoClient) -> None:
        self.mongo_db = client.get_database("CostcoTW_API_Parser")
