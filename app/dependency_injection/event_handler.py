from fastapi import Depends
from app.dependency_injection.services import require_SubscriptionService
from app.event_handler.intergration import RegisterSubscriptionEventHandler, \
    RemoveSubscriberEventHandler, RemoveSubscriptionEventHandler


def require_event_handler(service=Depends(require_SubscriptionService)):

    root_handler = RegisterSubscriptionEventHandler(service)
    root_handler.set_next(RemoveSubscriptionEventHandler(
        service)).set_next(RemoveSubscriberEventHandler(service))

    return root_handler
