from os import getenv
from pymongo import MongoClient


def require_MongoClient():
    conn_str = getenv("mongo_conn_str")
    with MongoClient(conn_str) as client:
        print("connect mongo db")
        yield client
    print("mongo db disconnect")
