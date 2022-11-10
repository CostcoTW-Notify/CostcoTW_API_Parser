from fastapi import APIRouter
from app.services import SnapshotService, CostcoApiService
from app.repositories import SnapshotRepository

router = APIRouter(prefix='/snapshot')


@router.post('/execute')
async def snapshot_all_product():

    service = SnapshotService(SnapshotRepository(), CostcoApiService())

    result = await service.snapshot_all_products()

    return {
        'status': 'Done',
        'snapshot_count': len(result)
    }
