from app.repositories import ExecuteLogRepository, SubscriptionRepository, SnapshotRepository
from app.services import LineNotifyService
from app.utility.constant import DAILY_NEW_BEST_BUY, DAILY_NEW_ONSALE
from app.utility import DateTimeHelper, NotifyMessageHelper
from app.models.mongo.product import Product
from app.models.enums import SubscriptionType
from datetime import datetime


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

    async def process_daily_check(self, job_type: SubscriptionType):

        if (job_type != SubscriptionType.DailyNewOnsale and job_type != SubscriptionType.DailyNewBestBuy):
            raise Exception("Invalid job_type")

        type = DAILY_NEW_BEST_BUY if job_type == SubscriptionType.DailyNewBestBuy else DAILY_NEW_ONSALE

        if self.execute_log_repo.check_today_already_execute(type):
            error_msg = f"The scenario : {type} is already executed today.."
            error_msg += f"Today is {DateTimeHelper.get_today_with_timezone()}"
            raise Exception(error_msg)

        subscriber = self.subscription_repo.get_subscription(type)
        if len(subscriber) == 0:
            return

        items = self._detect_today_new_item(job_type)
        if len(items) == 0:
            return

        messages = [
            NotifyMessageHelper.build_new_onsale_item_notify_message(p)
            if job_type == SubscriptionType.DailyNewOnsale else
            NotifyMessageHelper.build_new_best_buy_item_notify_message(p)
            for p in items]

        self.line_notify_service.appendPendingMessage(
            [s['token'] for s in subscriber], messages)

        self.execute_log_repo.create_today_execute_log(type)

        return

    def _detect_today_new_item(self, job_type: SubscriptionType):

        yesterday_items = self.snapshot_repo.get_products(
            self._create_query_filter(
                job_type,
                gt=DateTimeHelper.get_today_with_timezone(-1),
                lt=DateTimeHelper.get_today_with_timezone()
            ))

        if (len(yesterday_items) == 0):
            return []

        today_items = self.snapshot_repo.get_products(
            self._create_query_filter(
                job_type,
                gt=DateTimeHelper.get_today_with_timezone(),
                lt=DateTimeHelper.get_today_with_timezone(+1)
            ))

        today_items_code = set([p['code'] for p in today_items])
        yesterday_items_code = set([p['code']
                                   for p in yesterday_items])

        today_new_items_code = today_items_code - yesterday_items_code

        today_new_items = filter(
            lambda p: p['code'] in today_new_items_code, today_items)

        return list(today_new_items)

    def _create_query_filter(self, job_type: SubscriptionType, gt: datetime, lt: datetime):
        if (job_type == SubscriptionType.DailyNewBestBuy):
            return {
                "snapshotTime": {
                    "$gt": gt,
                    "$lt": lt
                },
                "price": {
                    "$mod": [10, 7]
                }
            }
        elif (job_type == SubscriptionType.DailyNewOnsale):
            return {
                "snapshotTime": {
                    "$gt": gt,
                    "$lt": lt
                },
                "onSaleInfo": {"$ne": None}
            }
        else:
            raise Exception("Invalid job_type")
