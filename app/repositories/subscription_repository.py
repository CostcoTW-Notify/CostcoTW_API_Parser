from app.repositories.mongo_repository import MongoRepository
from app.models.mongo.subscription import Subscription
from pymongo.collection import Collection


class SubscriptionRepository(MongoRepository):

    def __init__(self) -> None:
        super().__init__()
        self.collection: Collection[Subscription] = self.mongo_db.get_collection(
            'Subscription')

    def get_subscription(self, type: str) -> list[Subscription]:

        query = {
            "subscriptionType": type
        }
        data = self.collection.find(query)
        result = list(data)
        return result

    def create_subscription(self, subscription: Subscription) -> bool:

        # insert or update
        result = self.collection.update_one(
            dict(subscription),
            {
                "$set": {
                    "token": subscription['token'],
                    "code": subscription['code'],
                    "subscriptionType": subscription['subscriptionType']
                }
            },
            True
        )
        return result.acknowledged

    def delete_subscription(self, subscription: Subscription) -> bool:

        result = self.collection.delete_many(subscription)
        return result.acknowledged

    def delete_by_token(self, token: str) -> bool:

        result = self.collection.delete_many({
            "token": token
        })
        return result.acknowledged
