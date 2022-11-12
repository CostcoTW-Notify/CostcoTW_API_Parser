from unittest.mock import MagicMock
from app.models.mongo.product import Product, StockStatus
import app.repositories.mongo_repository as MongoRepo
from pytest_mock import MockerFixture


def test_get_mongo_database_will_get_env_conn_str(mocker: MockerFixture):

    getenv = mocker.patch.object(MongoRepo, 'getenv',
                                 return_value='mongo_conn_str')
    mongo = mocker.patch.object(MongoRepo.MongoClient, 'get_default_database')

    MongoRepo.MongoRepository()._get_mongo_database()

    getenv.assert_called_once_with('mongo_conn_str')
    mongo.assert_called_once()


def test_get_snapshot_collection_will_get_env_collection_name(mocker: MockerFixture):

    getenv = mocker.patch.object(MongoRepo, 'getenv',
                                 return_value='collName')
    get_database = MagicMock()

    mocker.patch.object(
        MongoRepo.MongoRepository, '_get_mongo_database', return_value=get_database)

    mocker.patch.object(get_database, 'list_collection_names',
                        return_value=['collName', 'aa', 'bb'])

    MongoRepo.MongoRepository()._get_snapshot_collection()

    getenv.assert_called_once_with('snapshot_collection')


def test_insert_product_will_call_mongo_collection(mocker: MockerFixture):

    collection = MagicMock()
    mocker.patch.object(MongoRepo.MongoRepository,
                        '_get_snapshot_collection', return_value=collection)

    collection_insert = mocker.patch.object(collection, 'insert_one')
    prod = Product('', '', '', StockStatus(True), '')
    MongoRepo.MongoRepository().insert_product(prod)

    collection_insert.assert_called_once()


def test_insert_products_will_call_mongo_collection(mocker: MockerFixture):

    collection = MagicMock()
    mocker.patch.object(MongoRepo.MongoRepository,
                        '_get_snapshot_collection', return_value=collection)

    collection_insert = mocker.patch.object(collection, 'insert_many')
    prod = Product('', '', '', StockStatus(True), '')
    MongoRepo.MongoRepository().insert_products([prod])

    collection_insert.assert_called_once()
