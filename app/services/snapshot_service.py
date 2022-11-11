from app.services.costco_api_service import CostcoApiService
from app.repositories import SnapshotRepository
from app.utility.datetime_helper import DateTimeHelper


class SnapshotService:
    def __init__(self, repo: SnapshotRepository, service: CostcoApiService) -> None:
        self.snapshot_repo = repo
        self.costco_service = service

    async def snapshot_all_products(self) -> list:

        query_today_snapshot = {
            "snapshotTime": {
                "$gt": DateTimeHelper.get_today_with_timezone(),
                "$lt": DateTimeHelper.get_today_with_timezone(+1)
            },
        }
        count = self.snapshot_repo.count_products(query_today_snapshot)
        if (count > 0):
            raise Exception(
                f"There is already exists today's snapshot in the database. snapshot count:{count}")
        products = await self.costco_service.fetch_all_products()
        return self.snapshot_repo.insert_products(products)
