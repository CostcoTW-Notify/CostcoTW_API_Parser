import asyncio
import pytest
from pytest_mock import MockerFixture
from app.services.subscription_service import \
    SubscriptionService, SubscriptionRequest, RequestType, SubscriptionType


def test_create_new_subscription_will_call_subscription_repo_with_correct_params(
    mocker: MockerFixture
):
    subscription_repo = mocker.MagicMock()
    subscription_repo.create_subscription = mocker.MagicMock(return_value=True)
    service = SubscriptionService(subscription_repo)

    asyncio.run(service.create_new_subscription(SubscriptionRequest(
        code="123456",
        requestType=RequestType.Create,
        token="token",
        subscriptionType=SubscriptionType.InventoryCheck)))

    subscription_repo.create_subscription.assert_called_once_with(
        {
            'code': '123456',
            'subscriptionType': 'InventoryCheck',
            'token': 'token'
        })


def test_create_new_subscription_will_raise_exception_if_type_is_InventoryCheck_but_not_received_code(
    mocker: MockerFixture
):

    subscription_repo = mocker.MagicMock()
    subscription_repo.create_subscription = mocker.MagicMock(return_value=True)
    service = SubscriptionService(subscription_repo)

    with pytest.raises(Exception) as e:
        asyncio.run(service.create_new_subscription(SubscriptionRequest(
            requestType=RequestType.Create,
            token="token",
            subscriptionType=SubscriptionType.InventoryCheck,
            code=None)))

    subscription_repo.create_subscription.assert_not_called()


def test_delete_subscription_will_call_subscription_repo_with_correct_params(
    mocker: MockerFixture
):

    subscription_repo = mocker.MagicMock()
    subscription_repo.delete_subscription = mocker.MagicMock(return_value=True)
    service = SubscriptionService(subscription_repo)

    asyncio.run(service.delete_subscription(SubscriptionRequest(
        code="123456",
        requestType=RequestType.Delete,
        token="token",
        subscriptionType=SubscriptionType.InventoryCheck)))

    subscription_repo.delete_subscription.assert_called_once_with(
        {
            'code': '123456',
            'subscriptionType': 'InventoryCheck',
            'token': 'token'
        })


def test_delete_by_token_will_call_repo(mocker: MockerFixture):

    subscription_repo = mocker.MagicMock()
    subscription_repo.delete_by_token = mocker.MagicMock(return_value=True)
    service = SubscriptionService(subscription_repo)

    asyncio.run(service.delete_by_token("Token"))

    subscription_repo.delete_by_token.assert_called_once_with("Token")
