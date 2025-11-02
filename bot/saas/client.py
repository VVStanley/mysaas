from bot.http_client import AsyncClient
from bot.conf import settings
from bot.saas.models import User, UserCreate
import logging

logger = logging.getLogger(__name__)


class SaasClient(AsyncClient):

    async def get_user(self, telegram_id: int) -> User:
        return await self.get(path=f"/users/{telegram_id}/", expected_model=User)

    async def create_user(self, user: UserCreate) -> User:
        return await self.post(
            path="/users/", json=user.model_dump(), expected_model=User
        )


def saas_client() -> SaasClient:
    return SaasClient(
        base_url=settings.SAAS_API_URL,
        headers={
            "Authorization": settings.API_TOKEN,
            "Content-Type": "application/json",
        },
    )
