import pytest
from pytest_mock import MockerFixture
from app.services.daily_check_service import DailyCheckService, SubscriptionType
import asyncio


def test_process_daily_check_will_raise_if_already_executed_today(
    mocker: MockerFixture
):

    line_notify_service = mocker.MagicMock
    subscription_repo = mocker.MagicMock
    snapshot_repo = mocker.MagicMock
    execute_log_repo = mocker.MagicMock
    execute_log_repo.check_today_already_execute = mocker.MagicMock(
        return_value=True)

    service = DailyCheckService(
        line_notify_service,
        subscription_repo,
        snapshot_repo,
        execute_log_repo
    )

    # Action & Assert
    with pytest.raises(Exception) as ex:
        asyncio.run(service.process_daily_check(
            SubscriptionType.DailyNewBestBuy))

    assert True == ex.value.args[0].startswith(
        'The scenario : DailyNewBestBuy is already executed today..')


def test_process_daily_check_will_do_nothing_is_no_one_subscription(mocker: MockerFixture):

    line_notify_service = mocker.MagicMock
    line_notify_service.appendPendingMessage = mocker.AsyncMock
    subscription_repo = mocker.MagicMock
    snapshot_repo = mocker.MagicMock
    snapshot_repo.get_products = mocker.MagicMock
    execute_log_repo = mocker.MagicMock
    execute_log_repo.create_today_execute_log = mocker.MagicMock
    execute_log_repo.check_today_already_execute = mocker.MagicMock(
        return_value=False)

    subscription_repo.get_subscription = mocker.MagicMock(return_value=[])

    service = DailyCheckService(
        line_notify_service,
        subscription_repo,
        snapshot_repo,
        execute_log_repo
    )

    # Action
    asyncio.run(service.process_daily_check(SubscriptionType.DailyNewBestBuy))

    # Assert
    snapshot_repo.get_products.assert_not_called
    line_notify_service.appendPendingMessage.assert_not_called
    execute_log_repo.create_today_execute_log.assert_not_called


def test_process_daily_check_will_call_appendPendingMessage_and_create_executed_log(
    mocker: MockerFixture
):

    line_notify_service = mocker.MagicMock()
    line_notify_service.appendPendingMessage = mocker.AsyncMock()
    subscription_repo = mocker.MagicMock()
    snapshot_repo = mocker.MagicMock()
    execute_log_repo = mocker.MagicMock()
    execute_log_repo.create_today_execute_log = mocker.MagicMock()
    execute_log_repo.check_today_already_execute = mocker.MagicMock(
        return_value=False)

    subscription_repo.get_subscription = mocker.MagicMock(
        return_value=[
            {
                "token": "token",
                "subscriptionType": "NewDailyBestBuy",
            }
        ])

    snapshot_repo.get_products = mocker.Mock()
    snapshot_repo.get_products.side_effect = [
        [{"code": "11111"}],  # yesterdat item
        [
            {
                "code": "22222",
                "onSaleInfo": {
                    "basePrice": 888,
                    "discountPrice": 111
                },
                "price": 777,
                "zhName": "ItemName",
                "url": "https://www.google.com"

            }
        ],  # today new item
    ]

    service = DailyCheckService(
        line_notify_service,
        subscription_repo,
        snapshot_repo,
        execute_log_repo
    )

    # Action
    asyncio.run(service.process_daily_check(SubscriptionType.DailyNewBestBuy))

    # Assert
    line_notify_service.appendPendingMessage.assert_called_once()
    execute_log_repo.create_today_execute_log.assert_called_once()

    pass
