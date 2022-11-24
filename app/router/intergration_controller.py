from fastapi import APIRouter, Depends
from base64 import b64decode
from json import loads
from app.models.events.pub_sub_event import PubSubEvent
from app.dependency_injection.event_handler import require_event_handler
from app.event_handler.intergration.event_handler import EventHandler


router = APIRouter(prefix='/intergration')


@router.post('/event')
async def process_intergration_event(
    model: PubSubEvent,
    event_handler: EventHandler = Depends(require_event_handler)
):

    event = loads(b64decode(model.message.data))

    await event_handler.handle_event(model.message.attributes.eventType, event)

    return {
        'status': 'Done'
    }
