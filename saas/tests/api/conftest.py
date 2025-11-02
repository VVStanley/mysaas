import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from tariff.models import Tariff

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(telegram_id=123, telegram_username="testuser")


@pytest.fixture
def authorized_client(api_client):
    api_client.credentials(HTTP_AUTHORIZATION=settings.API_TOKEN)
    return api_client


@pytest.fixture
def tariff():
    return Tariff.objects.create(name="Free", price=0)


@pytest.fixture
def telegram_id() -> int:
    return 123456789
