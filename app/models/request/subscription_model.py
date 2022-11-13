from pydantic import BaseModel
from typing import Optional
from enum import Enum


class RequestType(Enum):
    Unknown = 0
    Create = 1
    Delete = 2


class SubscriptionType(Enum):
    Unknown = 0
    DailyNewBestBuy = 1
    DailyNewOnsale = 2
    InventoryCheck = 3


class SubscriptionRequest(BaseModel):
    requestType: RequestType
    token: str
    subscriptionType: Optional[SubscriptionType]
    code: Optional[str]
