import asyncio
from pytest_mock import MockerFixture
from app.services.line_notify_service import LineNotifyService


def test_appendPendingMessage_will_send_request_to_microservice_endpoint(
    mocker: MockerFixture
):

    mock_publisher = mocker.MagicMock()
    mock_publisher.publish = mocker.MagicMock()
    mocker.patch(
        "app.services.line_notify_service.PublisherClient", return_value=mock_publisher)

    service = LineNotifyService()

    service.appendPendingMessage(
        ["token1", "token2"], ["message1", "message2"])

    assert 4 == mock_publisher.publish.call_count
