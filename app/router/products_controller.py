from fastapi import APIRouter
from app.services import SnapshotService, CostcoApiService, DailyCheckService, LineNotifyService
from app.repositories import SnapshotRepository, SubscriptionRepository, ExecuteLogRepository

router = APIRouter(prefix='/products')


@router.post('/snapshot')
async def snapshot_all_product():

    service = SnapshotService(SnapshotRepository(), CostcoApiService())

    result = await service.snapshot_all_products()

    return {
        'status': 'Done',
        'snapshot_count': len(result)
    }


@router.get('/new_best_buy')
async def detect_today_new_best_buy_item():

    service = DailyCheckService(line_notify_service=LineNotifyService(),
                                snapshot_repo=SnapshotRepository(),
                                subscription_repo=SubscriptionRepository(),
                                execute_log_repo=ExecuteLogRepository())
    items = service._detect_today_new_best_buy_items()

    result = [{
        "code": p['code'],
        "name": p['zhName'],
        "price": p['price']
    } for p in items]

    return {
        "count": len(result),
        "products": result
    }


@router.get('/new_onsale')
async def detect_today_new_onsale_item():

    service = DailyCheckService(line_notify_service=LineNotifyService(),
                                snapshot_repo=SnapshotRepository(),
                                subscription_repo=SubscriptionRepository(),
                                execute_log_repo=ExecuteLogRepository())
    items = service._detect_today_new_onsale_items()

    result = [{
        "code": p['code'],
        "name": p['zhName'],
        "price": p['price']
    } for p in items]

    return {
        "count": len(result),
        "products": result
    }
