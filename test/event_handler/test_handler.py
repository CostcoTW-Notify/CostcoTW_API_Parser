import asyncio
from pytest_mock import MockerFixture
from app.event_handler.intergration import RegisterSubscriptionEventHandler, \
    RemoveSubscriberEventHandler, RemoveSubscriptionEventHandler
from app.models.events.intergration.remove_subscriber_event import RemoveSubscriberEvent, EVENT_TYPE


def test_event_handler_chain(
    mocker: MockerFixture
):
    service = mocker.MagicMock()
    root_handler = RegisterSubscriptionEventHandler(service)
    root_handler.set_next(RemoveSubscriptionEventHandler(
        service)).set_next(RemoveSubscriberEventHandler(service))

    event = RemoveSubscriberEvent(
        Subscriber="token123",
        SubscriberType="LineNotify"
    )

    service.delete_by_token = mocker.AsyncMock()

    asyncio.run(root_handler.handle_event(EVENT_TYPE, event))

    service.delete_by_token.assert_called_once_with("token123")
