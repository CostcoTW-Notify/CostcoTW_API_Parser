from typing import TypedDict
from datetime import datetime


class InventoryCheck(TypedDict):
    code: str
    lastCheckStockCount: int
    lastCheckDateTime: datetime
