from typing import TypedDict, Optional


class Subscription(TypedDict):
    token: str
    subscriptionType: str
    code: Optional['str']
