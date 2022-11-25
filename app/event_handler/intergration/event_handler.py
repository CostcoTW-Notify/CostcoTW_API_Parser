from __future__ import annotations
from abc import ABC, abstractmethod


class EventHandler(ABC):

    def __init__(self) -> None:
        self.next_handler = None

    def set_next(self, handler: EventHandler) -> EventHandler:
        self.next_handler = handler
        return handler

    @abstractmethod
    async def handle_event(self, eventType: str, event):
        if self.next_handler:
            return await self.next_handler.handle_event(eventType, event)
        pass
