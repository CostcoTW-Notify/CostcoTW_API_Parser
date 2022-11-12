from fastapi import APIRouter, HTTPException
from app.repositories import SnapshotRepository, ExecuteLogRepository, SubscriptionRepository
from app.services import ProductInfoService, SubscriptionService, LineNotifyService
from app.models.request.execute_model import ExecuteModel
from app.models.request.subscription_model import SubscriptionRequest
from app.models.request.token_model import TokenModel
from app.utility.constant import DAILY_NEW_BEST_BUY, DAILY_NEW_ONSALE, INVENTORY_CHECK

router = APIRouter(prefix='/subscription')


@router.post('/process')
async def process_specific_scenario(model: ExecuteModel):
    ensure_subscription_type(model.SubscriptionType)

    service = SubscriptionService(
        ProductInfoService(SnapshotRepository()),
        LineNotifyService(),
        SubscriptionRepository(),
        ExecuteLogRepository())

    if model.SubscriptionType == DAILY_NEW_ONSALE:
        await service.process_daily_new_onsale_subscription()
    elif model.SubscriptionType == DAILY_NEW_BEST_BUY:
        await service.process_daily_new_best_buy_subscription()
    elif model.SubscriptionType == INVENTORY_CHECK:
        pass

    return {
        'status': 'Done'
    }


@router.post('/')
async def create_subscription(model: SubscriptionRequest):
    ensure_subscription_type(model.type)

    service = SubscriptionService(
        ProductInfoService(SnapshotRepository()),
        LineNotifyService(),
        SubscriptionRepository(),
        ExecuteLogRepository())

    if (model.type == INVENTORY_CHECK and model.code is None):
        raise HTTPException(status_code=400, detail="Missing 'code'")

    result = await service.create_new_subscription(model)

    if result:
        return {
            'status': 'success'
        }
    else:
        raise HTTPException(status_code=400, detail="service result is False")


@router.delete('/')
async def delete_subscription(model: SubscriptionRequest):
    ensure_subscription_type(model.type)

    service = SubscriptionService(
        ProductInfoService(SnapshotRepository()),
        LineNotifyService(),
        SubscriptionRepository(),
        ExecuteLogRepository())

    if (model.type == INVENTORY_CHECK and model.code is None):
        raise HTTPException(status_code=400, detail="Missing 'code'")

    result = await service.delete_subscription(model)
    if result:
        return {
            'status': 'success'
        }
    else:
        raise HTTPException(status_code=400, detail="service result is False")


@router.delete('/token')
async def delete_token(model: TokenModel):
    service = SubscriptionService(
        ProductInfoService(SnapshotRepository()),
        LineNotifyService(),
        SubscriptionRepository(),
        ExecuteLogRepository())

    result = await service.delete_by_token(model.token)

    if not result:
        raise HTTPException(status_code=400, detail="service result is False")

    return {
        'status': 'success'
    }


def ensure_subscription_type(type: str):
    if type != DAILY_NEW_BEST_BUY and \
       type != DAILY_NEW_ONSALE and \
       type != INVENTORY_CHECK:
        raise HTTPException(status_code=400, detail="type is invalid.")
