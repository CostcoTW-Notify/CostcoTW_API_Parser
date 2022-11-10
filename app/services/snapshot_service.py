from app.services.product_parser import fetch_all_products
from app.repositories import SnapshotRepository


async def snapshot_all_products() -> list:

    products = await fetch_all_products()
    repo = SnapshotRepository()
    return repo.insert_products(products)
