from fastapi import APIRouter
from app import services

router = APIRouter(prefix='/snapshot')


@router.post('/execute')
async def snapshot_all_product():

    result = await services.snapshot_all_products()
    return {
        'status': 'Done',
        'snapshot_count': len(result)
    }
