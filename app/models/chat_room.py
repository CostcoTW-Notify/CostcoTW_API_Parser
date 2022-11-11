from typing import TypedDict


class Subscriptions(TypedDict):
    DailyNewOnSale: bool
    DailyNewBestBuy: bool


class ChatRoom(TypedDict):
    Token: str
    Subscriptions: Subscriptions
