from fastapi import APIRouter, Depends
from app.services import SnapshotService, DailyCheckService
from app.models.enums import SubscriptionType
from app.dependency_injection.services import \
    require_SnapshotService, require_DailyCheckService
router = APIRouter(prefix='/products')


@router.post('/snapshot')
async def snapshot_all_product(
    service: SnapshotService = Depends(require_SnapshotService)
):

    result = await service.snapshot_all_products()

    return {
        'status': 'Done',
        'snapshot_count': len(result)
    }


@router.get('/new_best_buy')
async def detect_today_new_best_buy_item(
    service: DailyCheckService = Depends(require_DailyCheckService)
):

    items = service._detect_today_new_item(
        job_type=SubscriptionType.DailyNewBestBuy)

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
async def detect_today_new_onsale_item(
    service: DailyCheckService = Depends(require_DailyCheckService)
):

    items = service._detect_today_new_item(
        job_type=SubscriptionType.DailyNewOnsale)

    result = [{
        "code": p['code'],
        "name": p['zhName'],
        "price": p['price']
    } for p in items]

    return {
        "count": len(result),
        "products": result
    }
