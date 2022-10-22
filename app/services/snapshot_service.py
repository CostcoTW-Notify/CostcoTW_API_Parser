from app.services.product_parser import fetch_all_products
from app.repositories import MongoRepository


async def snapshot_all_products():

    products = await fetch_all_products()
    mongo = MongoRepository()
    return mongo.insert_products(products)
