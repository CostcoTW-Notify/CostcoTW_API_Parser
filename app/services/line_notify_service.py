from os import getenv
import httpx


class LineNotifyService:

    def __init__(self) -> None:
        self.line_notify_endpoint = getenv(
            'append_line_notify_endpoint')
        pass

    async def appendPendingMessage(self, token: list[str], messages: list[str]) -> None:
        
        if (self.line_notify_endpoint is None):
            raise Exception("Missing append_line_notify_endpoint")

        print(f"send append pending message request...")

        async with httpx.AsyncClient() as client:
            client.timeout = httpx.Timeout(10)
            response = await client.post(self.line_notify_endpoint, json={
                "tokens": token,
                "messages": messages
            })
            if response.status_code != 200 and response.status_code != 201:
                raise Exception("Send message to line-notify-sender fail...")
