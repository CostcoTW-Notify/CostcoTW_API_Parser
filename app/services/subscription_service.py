from app.repositories import SubscriptionRepository
from app.models.request.subscription_model import SubscriptionRequest


class SubscriptionService:

    def __init__(self,
                 subscription_repo: SubscriptionRepository) -> None:
        self.subscription_repo = subscription_repo

    async def create_new_subscription(self, subscription: SubscriptionRequest) -> bool:

        result = self.subscription_repo.create_subscription({
            "code": subscription.code,
            "subscriptionType": subscription.type,
            "token": subscription.token
        })
        return result

    async def delete_subscription(self, subscription: SubscriptionRequest) -> bool:

        result = self.subscription_repo.delete_subscription({
            "code": subscription.code,
            "subscriptionType": subscription.type,
            "token": subscription.token
        })
        return result

    async def delete_by_token(self, token: str) -> bool:

        result = self.subscription_repo.delete_by_token(token)
        return result
