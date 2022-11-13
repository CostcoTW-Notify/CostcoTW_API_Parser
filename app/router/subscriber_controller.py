from fastapi import APIRouter, HTTPException
from app.repositories import SnapshotRepository, ExecuteLogRepository, SubscriptionRepository, InventoryCheckRepository
from app.services import DailyCheckService, SubscriptionService, LineNotifyService, InventoryCheckService, CostcoApiService
from app.models.request.execute_model import ExecuteModel
from app.models.request.subscription_model import SubscriptionRequest, RequestType, SubscriptionType
from app.models.request.token_model import TokenModel
from app.utility.constant import DAILY_NEW_BEST_BUY, DAILY_NEW_ONSALE, INVENTORY_CHECK

router = APIRouter(prefix='/subscription')


def ensure_subscription_type(type: str):
    if type != DAILY_NEW_BEST_BUY and \
       type != DAILY_NEW_ONSALE and \
       type != INVENTORY_CHECK:
        raise HTTPException(status_code=400, detail="type is invalid.")


@router.post('/process')
async def process_specific_scenario(model: ExecuteModel):
    ensure_subscription_type(model.SubscriptionType)

    if model.SubscriptionType == DAILY_NEW_ONSALE:
        service = DailyCheckService(line_notify_service=LineNotifyService(),
                                    snapshot_repo=SnapshotRepository(),
                                    subscription_repo=SubscriptionRepository(),
                                    execute_log_repo=ExecuteLogRepository())
        await service.process_daily_new_onsale_subscription()
    elif model.SubscriptionType == DAILY_NEW_BEST_BUY:
        service = DailyCheckService(line_notify_service=LineNotifyService(),
                                    snapshot_repo=SnapshotRepository(),
                                    subscription_repo=SubscriptionRepository(),
                                    execute_log_repo=ExecuteLogRepository())
        await service.process_daily_new_best_buy_subscription()
    elif model.SubscriptionType == INVENTORY_CHECK:
        service = InventoryCheckService(costco_api_service=CostcoApiService(),
                                        line_notify_service=LineNotifyService(),
                                        inventory_check_repo=InventoryCheckRepository(),
                                        subscription_repo=SubscriptionRepository())

        await service.process_inventory_check()

    return {
        'status': 'Done'
    }


@router.patch('')
async def change_subscription(model: SubscriptionRequest):

    if model.requestType == RequestType.Unknown:
        raise Exception("Invalid 'requestType'")

    if (model.subscriptionType == SubscriptionType.Unknown):
        raise Exception("Invalid 'subscriptionType")

    if model.requestType == RequestType.Create:
        if model.subscriptionType == SubscriptionType.InventoryCheck and model.code is None:
            raise Exception("Invalid 'code'")

    process_result: bool
    service = SubscriptionService(SubscriptionRepository())

    if model.requestType == RequestType.Create:
        process_result = await service.create_new_subscription(model)

    elif model.requestType == RequestType.Delete and model.subscriptionType is None:
        process_result = await service.delete_by_token(model.token)

    elif model.requestType == RequestType.Delete and model.subscriptionType is not None:
        process_result = await service.delete_subscription(model)

    else:
        raise (Exception("Unknown error"))

    if process_result:
        return {
            'status': 'success'
        }
    else:
        raise HTTPException(status_code=400, detail="service result is False")
