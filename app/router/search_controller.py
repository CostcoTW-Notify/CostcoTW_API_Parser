from fastapi import APIRouter
from app import services

router = APIRouter(prefix='/search')


@router.get('/count_hot_buys_products')
async def count_hot_buys_category():

    category_count = await services.fetch_category_products('hot-buys')

    return {
        'status': '200',
        'category_count': len(category_count)
    }
