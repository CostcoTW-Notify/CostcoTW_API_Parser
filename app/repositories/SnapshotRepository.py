from pymongo.collection import Collection
from app.repositories.MongoRepository import MongoRepository
from app.models import Product


class SnapshotRepository(MongoRepository):

    def __init__(self) -> None:
        super().__init__()
        self.collection: Collection[Product] = self.mongo_db.get_collection(
            "DailySnapshot")

    def insert_product(self, product: Product):

        result = self.collection.insert_one(dict(product))
        return result.inserted_id

    def insert_products(self, products: list[Product]) -> list:

        products_dict = [dict(p) for p in products]
        result = self.collection.insert_many(products_dict)
        return result.inserted_ids