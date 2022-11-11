from app.repositories import SnapshotRepository
from app.utility.datetime_helper import DateTimeHelper
from app.models import Product


class ProductInfoService:

    def __init__(self, repo: SnapshotRepository) -> None:
        self.snapshot_repo = repo

    def detect_today_new_onsale_items(self) -> list[Product]:
        query_yesterday_onsale_item = {
            "snapshotTime": {
                "$gt": DateTimeHelper.get_today_with_timezone(-1),
                "$lt": DateTimeHelper.get_today_with_timezone()
            },
            "onSaleInfo": {"$ne": None}
        }

        yesterday_onsale_items = self.snapshot_repo.get_products(
            query_yesterday_onsale_item)

        if (len(yesterday_onsale_items) == 0):
            return []

        query_today_onsale_item = {
            "snapshotTime": {
                "$gt": DateTimeHelper.get_today_with_timezone(),
                "$lt": DateTimeHelper.get_today_with_timezone(+1)
            },
            "onSaleInfo": {"$ne": None}
        }

        today_onsale_items = self.snapshot_repo.get_products(
            query_today_onsale_item)

        today_items_code = set([p['code'] for p in today_onsale_items])
        yesterday_items_code = set([p['code'] for p in yesterday_onsale_items])

        today_new_items_code = today_items_code - yesterday_items_code

        today_new_items = filter(
            lambda p: p['code'] in today_new_items_code, today_onsale_items)

        return list(today_new_items)

    def detect_today_new_best_buy_items(self) -> list[Product]:
        query_yesterday_best_buy_item = {
            "snapshotTime": {
                "$gt": DateTimeHelper.get_today_with_timezone(-1),
                "$lt": DateTimeHelper.get_today_with_timezone()
            },
            "price": {
                "$mod": [10, 7]
            }
        }

        yesterday_best_buy_items = self.snapshot_repo.get_products(
            query_yesterday_best_buy_item)

        if (len(yesterday_best_buy_items) == 0):
            return []

        query_today_best_buy_item = {
            "snapshotTime": {
                "$gt": DateTimeHelper.get_today_with_timezone(),
                "$lt": DateTimeHelper.get_today_with_timezone(+1)
            },
            "price": {
                "$mod": [10, 7]
            }
        }

        today_best_buy_items = self.snapshot_repo.get_products(
            query_today_best_buy_item)

        today_items_code = set([p['code'] for p in today_best_buy_items])
        yesterday_items_code = set([p['code']
                                   for p in yesterday_best_buy_items])

        today_new_items_code = today_items_code - yesterday_items_code

        today_new_items = filter(
            lambda p: p['code'] in today_new_items_code, today_best_buy_items)

        return list(today_new_items)

    def check_items_inventory(self):
        return NotImplemented
