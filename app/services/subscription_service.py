from app.repositories import SubscriptionRepository
from app.models.request.subscription_model import SubscriptionRequest, SubscriptionType, RequestType
from app.utility.constant import DAILY_NEW_BEST_BUY, DAILY_NEW_ONSALE, INVENTORY_CHECK


class SubscriptionService:

    def __init__(self,
                 subscription_repo: SubscriptionRepository) -> None:
        self.subscription_repo = subscription_repo

    async def create_new_subscription(self, subscription: SubscriptionRequest) -> bool:
        if (subscription.requestType != RequestType.Create):
            raise Exception("Invalid 'requestType'")

        if (subscription.subscriptionType is None):
            raise Exception("Invalid 'subscriptionType'")

        if subscription.subscriptionType == SubscriptionType.InventoryCheck and subscription.code is None:
            raise Exception("Missing 'code'")

        result = self.subscription_repo.create_subscription({
            "code": subscription.code,
            "subscriptionType": self._map_subscription_type(subscription.subscriptionType),
            "token": subscription.token
        })
        return result

    async def delete_subscription(self, subscription: SubscriptionRequest) -> bool:
        if subscription.requestType != RequestType.Delete:
            raise Exception("Invalid 'requestType'")

        if subscription.subscriptionType is None:
            raise Exception("Invalid 'subscriptionType'")

        if subscription.subscriptionType == SubscriptionType.InventoryCheck and subscription.code is None:
            raise Exception("Missing 'code'")

        result = self.subscription_repo.delete_subscription({
            "code": subscription.code,
            "subscriptionType": self._map_subscription_type(subscription.subscriptionType),
            "token": subscription.token
        })
        return result

    async def delete_by_token(self, token: str) -> bool:

        result = self.subscription_repo.delete_by_token(token)
        return result

    def _map_subscription_type(self, subscription_type: SubscriptionType) -> str:

        if subscription_type == SubscriptionType.DailyNewOnsale:
            return DAILY_NEW_ONSALE
        if subscription_type == SubscriptionType.DailyNewBestBuy:
            return DAILY_NEW_BEST_BUY
        if subscription_type == SubscriptionType.InventoryCheck:
            return INVENTORY_CHECK
        else:
            return "Unknown"
