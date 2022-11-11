from fastapi import APIRouter
from app.services import CostcoApiService

router = APIRouter(prefix='/search')


@router.get('/count_hot_buys_products')
async def count_hot_buys_category():

    service = CostcoApiService()
    category_count = await service.fetch_category_products('hot-buys')

    return {
        'status': '200',
        'category_count': len(category_count)
    }
