from app.repositories import ExecuteLogRepository, SubscriptionRepository, SnapshotRepository
from app.services import LineNotifyService
from app.utility.constant import DAILY_NEW_BEST_BUY, DAILY_NEW_ONSALE
from app.utility import DateTimeHelper, NotifyMessageHelper
from app.models.mongo.product import Product


class DailyCheckService:

    def __init__(self,
                 line_notify_service: LineNotifyService,
                 subscription_repo: SubscriptionRepository,
                 snapshot_repo: SnapshotRepository,
                 execute_log_repo: ExecuteLogRepository) -> None:
        self.line_notify_service = line_notify_service
        self.subscription_repo = subscription_repo
        self.snapshot_repo = snapshot_repo
        self.execute_log_repo = execute_log_repo

    async def process_daily_new_onsale_subscription(self) -> None:

        if self.execute_log_repo.check_today_already_execute(DAILY_NEW_ONSALE):
            error_msg = f"The scenario : {DAILY_NEW_ONSALE} is already executed today.."
            error_msg += f"Today is {DateTimeHelper.get_today_with_timezone()}"
            raise Exception(error_msg)

        subscriber = self.subscription_repo.get_subscription(DAILY_NEW_ONSALE)
        if len(subscriber) == 0:
            return

        items = self._detect_today_new_onsale_items()
        if len(items) == 0:
            return

        messages = [
            NotifyMessageHelper.build_new_onsale_item_notify_message(p) for p in items]

        await self.line_notify_service.appendPendingMessage([s['token'] for s in subscriber], messages)

        self.execute_log_repo.create_today_execute_log(DAILY_NEW_ONSALE)

        return

    async def process_daily_new_best_buy_subscription(self) -> None:

        if self.execute_log_repo.check_today_already_execute(DAILY_NEW_BEST_BUY):
            error_msg = f"The scenario : {DAILY_NEW_BEST_BUY} is already executed today.."
            error_msg += f"Today is {DateTimeHelper.get_today_with_timezone()}"
            raise Exception(error_msg)

        subscriber = self.subscription_repo.get_subscription(
            DAILY_NEW_BEST_BUY)
        if len(subscriber) == 0:
            return

        items = self._detect_today_new_best_buy_items()
        if len(items) == 0:
            return

        messages = [
            NotifyMessageHelper.build_new_best_buy_item_notify_message(p) for p in items]

        await self.line_notify_service.appendPendingMessage(
            [s['token'] for s in subscriber], messages)

        self.execute_log_repo.create_today_execute_log(DAILY_NEW_BEST_BUY)
        return

    def _detect_today_new_onsale_items(self) -> list[Product]:
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

    def _detect_today_new_best_buy_items(self) -> list[Product]:
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
