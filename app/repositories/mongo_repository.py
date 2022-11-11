import abc
from typing import Optional
from pymongo import MongoClient
from os import getenv


class MongoRepository(abc.ABC):

    def __init__(self, database: Optional[str] = None) -> None:
        mongo_conn_str = getenv('mongo_conn_str')
        client = MongoClient(mongo_conn_str)

        if database is None:
            mongo_db = client.get_database("CostcoTW_API_Parser")
        else:
            mongo_db = client.get_database(database)

        self.mongo_db = mongo_db
