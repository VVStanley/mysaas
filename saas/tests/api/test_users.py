import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from users.serializers import UserSerializer

User = get_user_model()


@pytest.mark.django_db
def test_user_create(authorized_client, telegram_id):
    url = reverse("user-create")
    data = {"telegram_id": telegram_id, "telegram_username": "test_user"}

    response = authorized_client.post(url, data)

    user = User.objects.get(telegram_id=telegram_id)

    assert response.data == UserSerializer(user).data
