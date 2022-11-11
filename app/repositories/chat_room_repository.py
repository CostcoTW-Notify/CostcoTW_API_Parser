from pymongo.collection import Collection
from pymongo import MongoClient
from app.repositories.mongo_repository import MongoRepository
from app.models.chat_room import ChatRoom


class ChatRoomRepository(MongoRepository):

    def __init__(self) -> None:
        super().__init__("LineChatRoom-Service")
        self.collection: Collection[ChatRoom] = self.mongo_db.get_collection(
            "ChatRooms")

    def get_daily_new_onsale_subscriber(self) -> list[ChatRoom]:
        query = {
            "Subscriptions.DailyNewOnSale": True
        }

        result = self.collection.find(query)
        return list(result)

    def get_daily_new_best_buy_subscriber(self) -> list[ChatRoom]:
        query = {
            "Subscriptions.DailyNewBestBuy": True
        }

        result = self.collection.find(query)
        return list(result)
