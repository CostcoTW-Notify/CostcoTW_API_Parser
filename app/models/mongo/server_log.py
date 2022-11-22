from typing import TypedDict, Optional, Any
from datetime import datetime


class HttpRequest(TypedDict):
    path: str
    method: str
    body: Any


class ServerLog(TypedDict):
    request: HttpRequest
    response_status: int  # Http Status
    start_time: datetime
    process_time: int  # unit : ms
    error: Optional[str]
