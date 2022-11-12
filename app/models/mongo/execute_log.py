from typing import TypedDict
from datetime import datetime


class ExecuteLogModel(TypedDict):
    Type: str
    ExecuteDate: datetime
