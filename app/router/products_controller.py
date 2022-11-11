from fastapi import APIRouter
from app.services import SnapshotService, CostcoApiService
from app.repositories import SnapshotRepository
from app.services.product_info_service import ProductInfoService
from app.models.product import Product

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

    service = ProductInfoService(SnapshotRepository())
    items = service.detect_today_new_best_buy_items()

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

    service = ProductInfoService(SnapshotRepository())
    items = service.detect_today_new_on_sale_items()

    result = [{
        "code": p['code'],
        "name": p['zhName'],
        "price": p['price']
    } for p in items]

    return {
        "count": len(result),
        "products": result
    }
