from app.services.costco_api_service import CostcoApiService
from app.repositories import SnapshotRepository


class SnapshotService:
    def __init__(self, repo: SnapshotRepository, service: CostcoApiService) -> None:
        self.snapshot_repo = repo
        self.costco_service = service

    async def snapshot_all_products(self) -> list:
        products = await self.costco_service.fetch_all_products()
        return self.snapshot_repo.insert_products(products)
