from pydantic import BaseModel
from typing import Optional


class SubscriptionRequest(BaseModel):
    token: str
    type: str
    code: Optional[str]
