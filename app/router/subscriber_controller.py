from fastapi import APIRouter, HTTPException, Depends
from app.services import SubscriptionService, DailyCheckService, InventoryCheckService
from app.models.request.execute_model import ExecuteModel
from app.models.request.subscription_model import SubscriptionRequest, RequestType, SubscriptionType
from app.utility.constant import DAILY_NEW_BEST_BUY, DAILY_NEW_ONSALE, INVENTORY_CHECK
from app.dependency_injection.services \
    import require_DailyCheckService, require_InventoryCheckService, require_SubscriptionService
router = APIRouter(prefix='/subscription')


def ensure_subscription_type(type: str):
    if type != DAILY_NEW_BEST_BUY and \
       type != DAILY_NEW_ONSALE and \
       type != INVENTORY_CHECK:
        raise HTTPException(status_code=400, detail="type is invalid.")


@router.post('/process')
async def process_specific_scenario(
    model: ExecuteModel,
    daily_check_service: DailyCheckService = Depends(
        require_DailyCheckService),
    inventory_check_service: InventoryCheckService = Depends(
        require_InventoryCheckService)
):
    ensure_subscription_type(model.SubscriptionType)

    if model.SubscriptionType == DAILY_NEW_ONSALE:
        await daily_check_service.process_daily_new_onsale_subscription()
    elif model.SubscriptionType == DAILY_NEW_BEST_BUY:
        await daily_check_service.process_daily_new_best_buy_subscription()
    elif model.SubscriptionType == INVENTORY_CHECK:
        await inventory_check_service.process_inventory_check()

    return {
        'status': 'Done'
    }


@router.patch('')
async def change_subscription(
    model: SubscriptionRequest,
    service: SubscriptionService = Depends(require_SubscriptionService)
):

    if model.requestType == RequestType.Unknown:
        raise Exception("Invalid 'requestType'")

    if (model.subscriptionType == SubscriptionType.Unknown):
        raise Exception("Invalid 'subscriptionType")

    if model.requestType == RequestType.Create:
        if model.subscriptionType == SubscriptionType.InventoryCheck and model.code is None:
            raise Exception("Invalid 'code'")

    process_result: bool

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
