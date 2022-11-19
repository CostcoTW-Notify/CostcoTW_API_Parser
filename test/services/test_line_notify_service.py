import asyncio
from pytest_mock import MockerFixture
from app.services.line_notify_service import LineNotifyService, httpx


def test_appendPendingMessage_will_send_request_to_microservice_endpoint(
    mocker: MockerFixture
):

    service = LineNotifyService()
    service.line_notify_endpoint = "http://localhost:8000/LineNotifyEndpoint"

    httpx.AsyncClient = mocker.MagicMock()
    mock_client = mocker.MagicMock()
    mock_client.post = mocker.AsyncMock(return_value=httpx.Response(200))
    httpx.AsyncClient.return_value.__aenter__.return_value = mock_client
    asyncio.run(service.appendPendingMessage(
        ["token1", "token2"], ["message1", "message2"]))

    mock_client.post.assert_called_once()
