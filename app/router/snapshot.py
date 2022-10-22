from fastapi import APIRouter
from app.services import snapshot_all_products

router = APIRouter(prefix='/snapshot')


@router.post('/execute')
async def snapshot_all_product():
    result = await snapshot_all_products()
    return {
        'status': result
    }
