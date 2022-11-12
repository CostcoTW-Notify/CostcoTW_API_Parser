from app.repositories import ExecuteLogRepository, SubscriptionRepository
from app.services import ProductInfoService, LineNotifyService
from app.utility import NotifyMessageHelper, DateTimeHelper
from app.models.request.subscription_model import SubscriptionRequest
from app.utility.constant import DAILY_NEW_BEST_BUY, DAILY_NEW_ONSALE


class SubscriptionService:

    def __init__(self,
                 product_service: ProductInfoService,
                 line_notify_service: LineNotifyService,
                 subscription_repo: SubscriptionRepository,
                 execute_log_repo: ExecuteLogRepository) -> None:
        self.product_service = product_service
        self.line_notify_service = line_notify_service
        self.execute_log_repo = execute_log_repo
        self.subscription_repo = subscription_repo

    async def process_daily_new_onsale_subscription(self) -> None:

        if self.execute_log_repo.check_today_already_execute(DAILY_NEW_ONSALE):
            error_msg = f"The scenario : {DAILY_NEW_ONSALE} is already executed today.."
            error_msg += f"Today is {DateTimeHelper.get_today_with_timezone()}"
            raise Exception(error_msg)

        subscriber = self.subscription_repo.get_subscription(DAILY_NEW_ONSALE)
        if len(subscriber) == 0:
            return

        items = self.product_service.detect_today_new_onsale_items()
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

        items = self.product_service.detect_today_new_best_buy_items()
        if len(items) == 0:
            return

        messages = [
            NotifyMessageHelper.build_new_best_buy_item_notify_message(p) for p in items]

        await self.line_notify_service.appendPendingMessage(
            [s['token'] for s in subscriber], messages)

        self.execute_log_repo.create_today_execute_log(DAILY_NEW_BEST_BUY)
        return

    async def create_new_subscription(self, subscription: SubscriptionRequest) -> bool:

        result = self.subscription_repo.create_subscription({
            "code": subscription.code,
            "subscription_type": subscription.type,
            "token": subscription.token
        })
        return result

    async def delete_subscription(self, subscription: SubscriptionRequest) -> bool:

        result = self.subscription_repo.delete_subscription({
            "code": subscription.code,
            "subscription_type": subscription.type,
            "token": subscription.token
        })
        return result

    async def delete_by_token(self, token: str) -> bool:

        result = self.subscription_repo.delete_by_token(token)
        return result
