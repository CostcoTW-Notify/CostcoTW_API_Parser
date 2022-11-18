import pytest
from pytest_mock import MockerFixture
from app.services.snapshot_service import \
    SnapshotService, SnapshotRepository, CostcoApiService
import asyncio


def test_snapshot_all_products_will_insert_data_to_database(
    mocker: MockerFixture,
):

    repo = mocker.MagicMock()
    costco_service = mocker.MagicMock()
    fetch_method = mocker.AsyncMock()
    costco_service.fetch_all_products = fetch_method
    repo.count_products = mocker.MagicMock(return_value=0)
    service = SnapshotService(repo, costco_service)

    # action
    asyncio.run(service.snapshot_all_products())

    # assert
    assert fetch_method.call_count == 1
    assert repo.insert_products.call_count == 1


def test_snapshot_all_products_will_raise_exception_if_today_already_snapshot_products(
    mocker: MockerFixture
):

    repo = mocker.MagicMock()
    costco_service = mocker.MagicMock()
    fetch_method = mocker.AsyncMock()
    costco_service.fetch_all_products = fetch_method
    repo.count_products = mocker.MagicMock(return_value=1)
    service = SnapshotService(repo, costco_service)

    # action & assert
    with pytest.raises(Exception):
        asyncio.run(service.snapshot_all_products())
