from fastapi import APIRouter
from app.services.product_info_service import ProductInfoService
from app.repositories.chat_room_repository import ChatRoomRepository
from app.repositories.snapshot_repository import SnapshotRepository
from app.services.subscription_service import SubscriptionService
from app.services.line_notify_service import LineNotifyService

router = APIRouter(prefix='/subscriber')


@router.post('/daily_new_onsale/send_notify')
async def process_new_onsale_scenario():

    service = SubscriptionService(
        ChatRoomRepository(),
        ProductInfoService(SnapshotRepository()),
        LineNotifyService())

    result = await service.process_daily_new_onsale_subscription()

    return {
        'status': 'Done',
        'subscriber_count': result
    }
