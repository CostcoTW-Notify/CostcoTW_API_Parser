from app.event_handler.intergration.event_handler import EventHandler
from app.models.events.intergration.remove_subscription_event import RemoveSubscriptionEvent, EVENT_TYPE
from app.services.subscription_service \
    import SubscriptionService, SubscriptionRequest, RequestType, SubscriptionType
from app.utility.constant import DAILY_NEW_ONSALE, DAILY_NEW_BEST_BUY, INVENTORY_CHECK


class RemoveSubscriptionEventHandler(EventHandler):

    def __init__(self, service: SubscriptionService) -> None:
        super().__init__()
        self.service = service

    async def handle_event(self, eventType: str, event):
        if eventType == EVENT_TYPE:
            await self.process(event)

        await super().handle_event(eventType, event)

    async def process(self, event: RemoveSubscriptionEvent):
        if event['SubscriberType'] != "LineNotify":
            return

        type = SubscriptionType.Unknown
        if event['SubscriptionType'] == DAILY_NEW_ONSALE:
            type = SubscriptionType.DailyNewOnsale
        elif event['SubscriptionType'] == DAILY_NEW_BEST_BUY:
            type = SubscriptionType.DailyNewBestBuy
        elif event['SubscriptionType'] == INVENTORY_CHECK:
            type = SubscriptionType.InventoryCheck
        else:
            return

        request = SubscriptionRequest(
            code=event['Code'],
            requestType=RequestType.Delete,
            subscriptionType=type,
            token=event['Subscriber']
        )

        await self.service.delete_subscription(request)
        return
