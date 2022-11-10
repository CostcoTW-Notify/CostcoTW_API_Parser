import abc
from pymongo import MongoClient
from os import getenv


class MongoRepository(abc.ABC):

    def __init__(self) -> None:
        mongo_conn_str = getenv('mongo_conn_str')
        mongo_db = MongoClient(mongo_conn_str).get_database(
            "CostcoTW_API_Parser")
        self.mongo_db = mongo_db
