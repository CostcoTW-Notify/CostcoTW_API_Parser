from pydantic import BaseModel
from typing import Optional
from app.models.enums import RequestType, SubscriptionType


class SubscriptionRequest(BaseModel):
    requestType: RequestType
    token: str
    subscriptionType: Optional[SubscriptionType]
    code: Optional[str]
