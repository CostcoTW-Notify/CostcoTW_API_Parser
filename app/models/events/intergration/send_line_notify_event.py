from typing import TypedDict

EVENT_TYPE = "SendLineNotify"


class SendLineNotifyEvent(TypedDict):
    token: str
    message: str
