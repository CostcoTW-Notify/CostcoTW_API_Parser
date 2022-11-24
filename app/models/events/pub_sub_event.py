from pydantic import BaseModel


class EventAttributes(BaseModel):
    eventType: str
    application: str


class EventMessage(BaseModel):
    attributes: EventAttributes
    data: str
    messageId: str
    publishTime: str


class PubSubEvent(BaseModel):
    message: EventMessage
    subscription: str
