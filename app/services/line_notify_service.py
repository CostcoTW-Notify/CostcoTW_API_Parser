import httpx


class LineNotifyService:

    def __init__(self) -> None:
        self.line_notify_endpoint = 'https://line-notify-sender-q4d4kz5xwq-de.a.run.app/LineNotify/SendMessage'
        pass

    async def SendNotify(self, token: list[str], messages: list[str]) -> None:

        async with httpx.AsyncClient() as client:
            client.timeout = httpx.Timeout(10)

            for tk in token:
                for msg in messages:
                    response = await client.post(self.line_notify_endpoint, json={
                        "token": tk,
                        "message": msg
                    })
                    print(response.status_code)
