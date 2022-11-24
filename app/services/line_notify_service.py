from os import getenv
from google.cloud.pubsub_v1 import PublisherClient
from google.cloud.pubsub_v1.futures import Future
from json import dumps
from app.models.events.intergration.send_line_notify_event import SendLineNotifyEvent, EVENT_TYPE


class LineNotifyService:

    def __init__(self) -> None:
        self.publisher = PublisherClient()
        self.intergration_topic = getenv('gcp_intergration_topic_path') or ""

    def appendPendingMessage(self, token: list[str], messages: list[str]) -> None:

        for t in token:
            for m in messages:
                data = SendLineNotifyEvent(
                    token=t,
                    message=m
                )
                json = bytes(dumps(data), 'utf-8')
                task: Future = self.publisher.publish(
                    self.intergration_topic,
                    data=json,
                    eventType=EVENT_TYPE, application="CostcoTW-API-Parser")
                result = task.result()
