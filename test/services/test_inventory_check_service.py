from pytest_mock import MockFixture
from app.services.inventory_check_service import InventoryCheckService
from app.models.mongo.subscription import Subscription
from app.utility.constant import INVENTORY_CHECK
import asyncio


def test_process_inventory_check_will_call_appendPendingMessage(
    mocker: MockFixture
):

    costco_api_service = mocker.MagicMock()
    line_notify_service = mocker.MagicMock()
    inventory_check_repo = mocker.MagicMock()
    subscription_repo = mocker.MagicMock()

    fakeSubscription: Subscription = {
        "code": "123456",
        "subscriptionType": INVENTORY_CHECK,
        "token": "TokenToken"
    }

    subscription_repo.get_subscription = mocker.MagicMock(
        return_value=[fakeSubscription])

    line_notify_service.appendPendingMessage = mocker.AsyncMock()

    service = InventoryCheckService(
        costco_api_service,
        line_notify_service,
        inventory_check_repo,
        subscription_repo
    )

    service._check_items_inventory = mocker.AsyncMock(return_value={
        "code": "123456",
        "zhName": "ItemName",
        "price": 777,
        "stockStatus": {
                "inStock": True,
                "stockLevel": 10
        },
        "url": "https://www.google.com"
    })

    # Action
    asyncio.run(service.process_inventory_check())

    # Assert
    line_notify_service.appendPendingMessage.assert_awaited_once()


def test_check_items_inventory_will_fetch_info_from_costco_api_and_update_new_count(
    mocker: MockFixture
):

    costco_api_service = mocker.MagicMock()
    line_notify_service = mocker.MagicMock()
    inventory_check_repo = mocker.MagicMock()
    subscription_repo = mocker.MagicMock()

    costco_api_service._fetch_product_by_code = mocker.AsyncMock(
        return_value={
            "code": "123456",
            "zhName": "ItemName",
            "price": 777,
            "stockStatus": {
                "inStock": True,
                "stockLevel": 10
            }
        }
    )

    inventory_check_repo.update_inventory_check_count = mocker.MagicMock()
    inventory_check_repo.get_last_check_stock_count = mocker.MagicMock(
        return_value=0)

    service = InventoryCheckService(
        costco_api_service,
        line_notify_service,
        inventory_check_repo,
        subscription_repo
    )

    # Action
    result = asyncio.run(service._check_items_inventory("123456"))

    # Assert
    inventory_check_repo.update_inventory_check_count.assert_called_once_with(
        "123456", 10)
    costco_api_service._fetch_product_by_code.assert_called_once_with("123456")
    assert result is not None
