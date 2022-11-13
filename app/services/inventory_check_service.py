
from app.models.mongo.product import Product
from app.services import CostcoApiService, LineNotifyService
from app.repositories import InventoryCheckRepository, SubscriptionRepository
from app.utility import INVENTORY_CHECK, NotifyMessageHelper
import asyncio


class InventoryCheckService:

    def __init__(self,
                 costco_api_service: CostcoApiService,
                 line_notify_service: LineNotifyService,
                 inventory_check_repo: InventoryCheckRepository,
                 subscription_repo: SubscriptionRepository
                 ) -> None:
        self.costco_api_service = costco_api_service
        self.inventory_check_repo = inventory_check_repo
        self.subscription_repo = subscription_repo
        self.line_notify_service = line_notify_service

    async def process_inventory_check(self) -> None:
        subscriber = self.subscription_repo.get_subscription(INVENTORY_CHECK)

        codes = set([x['code'] for x in subscriber])

        tasks = []
        for code in codes:
            if (code is None):
                continue

            # 檢查是否需要通知，若無需通知則不回傳
            product = await self._check_items_inventory(code)
            if (product is None):
                continue

            message = NotifyMessageHelper.build_product_in_stock_notify_message(
                product)

            tokens = [i['token']
                      for i in filter(lambda x: x['code'] == code, subscriber)]

            tasks.append(self.line_notify_service.appendPendingMessage(
                tokens, [message]))

        if (len(tasks) > 0):
            await asyncio.wait(tasks)  # No need to check result
        pass

    async def _check_items_inventory(self, code: str) -> Product | None:
        product = await self.costco_api_service._fetch_product_by_code(code)

        last_check_count = self.inventory_check_repo.get_last_check_stock_count(
            code)

        if (product['stockStatus']["inStock"] == False):
            self.inventory_check_repo.update_inventory_check_count(code, 0)
            return None

        if (product['stockStatus']['stockLevel'] is None):
            self.inventory_check_repo.update_inventory_check_count(
                code, 999)  # 庫存充足
        else:
            self.inventory_check_repo.update_inventory_check_count(
                code, product['stockStatus']['stockLevel'])

        # 上次檢查是無庫存，這次轉換為有庫存則需要通知
        if (last_check_count != 0):
            return None

        return product
