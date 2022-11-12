from typing import TypedDict, Optional


class Subscription(TypedDict):
    token: str
    subscription_type: str
    code: Optional['str']
