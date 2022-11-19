from pytest_mock import MockerFixture
from app.repositories.subscription_repository import SubscriptionRepository, Subscription


def test_get_subscription_will_call_collectio_with_correct_param(
    mocker: MockerFixture
):

    mongo = mocker.MagicMock()
    mongo.name = "mongo"
    db = mocker.MagicMock()
    db.name = "db"
    collection = mocker.MagicMock()
    collection.name = "collection"
    collection.find = mocker.MagicMock()

    mongo.get_database = mocker.MagicMock(return_value=db)
    db.get_collection = mocker.MagicMock(return_value=collection)

    repo = SubscriptionRepository(mongo)

    repo.get_subscription(type="subsType")

    collection.find.assert_called_once_with({
        "subscriptionType": "subsType"
    })


def test_create_subscription_will_call_update_one_with_correct_params(
    mocker: MockerFixture
):
    mongo = mocker.MagicMock()
    mongo.name = "mongo"
    db = mocker.MagicMock()
    db.name = "db"
    collection = mocker.MagicMock()
    collection.name = "collection"
    collection.update_one = mocker.MagicMock()

    mongo.get_database = mocker.MagicMock(return_value=db)
    db.get_collection = mocker.MagicMock(return_value=collection)

    repo = SubscriptionRepository(mongo)

    repo.create_subscription(Subscription(
        token="Token",
        subscriptionType="subsType",
        code=None
    ))

    collection.update_one.assert_called_once_with(
        {'token': 'Token', 'subscriptionType': 'subsType', 'code': None},
        {'$set': {'token': 'Token', 'code': None, 'subscriptionType': 'subsType'}}, True)
