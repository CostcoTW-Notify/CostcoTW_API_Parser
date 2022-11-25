from typing import TypedDict, Optional, Final

EVENT_TYPE: Final[str] = "RemoveSubscription"


class RemoveSubscriptionEvent(TypedDict):
    SubscriberType: str  # eg. LineNotify , Email , WhatApp... etc.
    Subscriber: str  # LineNotify token ,email address... etc.

    SubscriptionType: str  # DailyNewOnSale, DailyBestBuy, InventoryCheck
    Code: Optional[str]
