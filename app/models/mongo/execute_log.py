from typing import TypedDict
from datetime import datetime


class ExecuteLogModel(TypedDict):
    type: str
    executeDate: datetime
