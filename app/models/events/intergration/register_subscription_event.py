from typing import TypedDict, Optional, Final

EVENT_TYPE: Final[str] = "RegisterSubscription"


class RegisterSubscriptionEvent(TypedDict):
    SubscriberType: str  # eg. LineNotify , Email , WhatApp... etc.
    Subscriber: str  # LineNotify token ,email address... etc.

    SubscriptionType: str
    Code: Optional[str]
