from pymongo import MongoClient
from app.models import Product
from os import getenv


class MongoRepository:

    def _get_mongo_database(self):

        mongo_conn_str = getenv('mongo_conn_str')
        mongo_db = MongoClient(mongo_conn_str).get_default_database()
        return mongo_db

    def _get_snapshot_collection(self):

        name = getenv('snapshot_collection')
        mongo_db = self._get_mongo_database()

        if name not in mongo_db.list_collection_names():
            raise KeyError(f'Mongo collection "{name}" not exist...')

        snapshot_collection = mongo_db.get_collection(name=name)
        return snapshot_collection

    def insert_product(self, product: Product):

        collection = self._get_snapshot_collection()
        result = collection.insert_one(product.to_dict())
        return result

    def insert_products(self, products: list[Product]):

        products_dict = [p.to_dict() for p in products]
        collection = self._get_snapshot_collection()
        result = collection.insert_many(products_dict)
        return result.acknowledged
