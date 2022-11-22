from os import getenv
from pymongo import MongoClient


def require_MongoClient():
    conn_str = getenv("mongo_conn_str")
    client = MongoClient(conn_str)
    try:
        print("connect mongo db")
        yield client
    finally:
        client.close()
        print("mongo db disconnect")
