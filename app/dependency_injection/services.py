from fastapi import Depends
from app.services.costco_api_service import CostcoApiService
from app.services.daily_check_service import DailyCheckService
from app.services.inventory_check_service import InventoryCheckService
from app.services.line_notify_service import LineNotifyService
from app.services.snapshot_service import SnapshotService
from app.services.subscription_service import SubscriptionService
from app.dependency_injection.repositories \
    import require_ExecuteLogRepository, require_InventoryRepository, \
    require_SnapshotRepository, require_SubscriptionRepository


def require_CostcoApiService():
    service = CostcoApiService()
    return service


def require_LineNotifyService():
    service = LineNotifyService()
    return service


def require_DailyCheckService(
    line_notify_service=Depends(require_LineNotifyService),
    subscription_repository=Depends(require_SubscriptionRepository),
    snapshot_repository=Depends(require_SnapshotRepository),
    execute_log_repository=Depends(require_ExecuteLogRepository)
):
    service = DailyCheckService(
        line_notify_service,
        subscription_repository,
        snapshot_repository,
        execute_log_repository)

    return service


def require_InventoryCheckService(
    costco_api_service=Depends(require_CostcoApiService),
    line_notify_service=Depends(require_LineNotifyService),
    inventory_check_repo=Depends(require_InventoryRepository),
    subscription_repo=Depends(require_SubscriptionRepository)
):
    service = InventoryCheckService(
        costco_api_service,
        line_notify_service,
        inventory_check_repo,
        subscription_repo)
    return service


def require_SnapshotService(
    costco_api_service=Depends(require_CostcoApiService),
    snapshot_repository=Depends(require_SnapshotRepository)
):
    service = SnapshotService(
        repo=snapshot_repository,
        service=costco_api_service
    )
    return service


def require_SubscriptionService(
    subscription_repo=Depends(require_SubscriptionRepository)
):
    service = SubscriptionService(subscription_repo)
    return service
