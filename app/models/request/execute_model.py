from pydantic import BaseModel


class ExecuteModel(BaseModel):
    SubscriptionType: str
