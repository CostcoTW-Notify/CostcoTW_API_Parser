from pytest_mock import MockerFixture
from app.services import snapshot_all_products
import app.services.snapshot_service as SnapshotService
import asyncio


def test_snapshot_all_products_will_call_correct_method(mocker: MockerFixture):

    fetch_all_products = mocker.patch.object(
        SnapshotService, 'fetch_all_products')

    insert_products = mocker.patch.object(
        SnapshotService.MongoRepository, 'insert_products')

    asyncio.run(snapshot_all_products())

    fetch_all_products.assert_called_once()
    insert_products.assert_called_once()
