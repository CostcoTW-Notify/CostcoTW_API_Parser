from pymongo import MongoClient
from app.dependency_injection.mongo import require_MongoClient
from app.repositories.subscription_repository import SubscriptionRepository
from app.repositories.inventory_check_repository import InventoryCheckRepository
from app.repositories.snapshot_repository import SnapshotRepository
from app.repositories.execute_log_repository import ExecuteLogRepository
from fastapi import Depends


def require_SubscriptionRepository(mongo: MongoClient = Depends(require_MongoClient)):
    repo = SubscriptionRepository(mongo)
    return repo


def require_InventoryRepository(mongo: MongoClient = Depends(require_MongoClient)):
    repo = InventoryCheckRepository(mongo)
    return repo


def require_SnapshotRepository(mongo: MongoClient = Depends(require_MongoClient)):
    repo = SnapshotRepository(mongo)
    return repo


def require_ExecuteLogRepository(mongo: MongoClient = Depends(require_MongoClient)):
    repo = ExecuteLogRepository(mongo)
    return repo
