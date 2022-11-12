import abc
from typing import Optional
from pymongo import MongoClient
from os import getenv


class MongoRepository(abc.ABC):

    def __init__(self) -> None:
        mongo_conn_str = getenv('mongo_conn_str')
        client = MongoClient(mongo_conn_str)
        self.mongo_db = client.get_database("CostcoTW_API_Parser")
