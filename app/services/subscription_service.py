from app.repositories.chat_room_repository import ChatRoomRepository
from app.services.product_info_service import ProductInfoService
from app.utility.notify_message_helper import NotifyMessageHelper
from app.services.line_notify_service import LineNotifyService


class SubscriptionService:

    def __init__(self,
                 repo: ChatRoomRepository,
                 product_service: ProductInfoService,
                 line_notify_service: LineNotifyService) -> None:
        self.product_service = product_service
        self.chat_room_repo = repo
        self.line_notify_service = line_notify_service

    async def process_daily_new_onsale_subscription(self) -> None:

        subscriber = self.chat_room_repo.get_daily_new_onsale_subscriber()
        if len(subscriber) == 0:
            return

        items = self.product_service.detect_today_new_onsale_items()
        if len(items) == 0:
            return

        messages = [
            NotifyMessageHelper.build_new_onsale_item_notify_message(p) for p in items]

        await self.line_notify_service.SendNotify([s['Token'] for s in subscriber], messages)

        return

    async def process_daily_new_best_buy_subscription(self) -> None:

        subscriber = self.chat_room_repo.get_daily_new_best_buy_subscriber()
        if len(subscriber) == 0:
            return

        items = self.product_service.detect_today_new_best_buy_items()
        if len(items) == 0:
            return

        messages = [
            NotifyMessageHelper.build_new_best_buy_item_notify_message(p) for p in items]

        await self.line_notify_service.SendNotify(
            [s['Token'] for s in subscriber], messages)

        return
