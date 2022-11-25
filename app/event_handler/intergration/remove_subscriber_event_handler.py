from app.event_handler.intergration.event_handler import EventHandler
from app.models.events.intergration.remove_subscriber_event import RemoveSubscriberEvent, EVENT_TYPE
from app.services.subscription_service import SubscriptionService


class RemoveSubscriberEventHandler(EventHandler):

    def __init__(self, service: SubscriptionService) -> None:
        super().__init__()
        self.service = service

    async def handle_event(self, eventType: str, event):
        if eventType == EVENT_TYPE:
            await self.process(event)

        await super().handle_event(eventType, event)

    async def process(self, event: RemoveSubscriberEvent):
        if event['SubscriberType'] != "LineNotify":
            return

        await self.service.delete_by_token(event['Subscriber'])
        return
