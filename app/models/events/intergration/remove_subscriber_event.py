from typing import TypedDict, Final

EVENT_TYPE: Final[str] = "RemoveSubscriber"


class RemoveSubscriberEvent(TypedDict):
    SubscriberType: str  # eg. LineNotify , Email , WhatApp... etc.
    Subscriber: str  # LineNotify token ,email address... etc.
