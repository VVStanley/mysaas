from django.urls import path

from .views import (
    UserCreateView,
    UserListView,
    UserByTelegramView,
)

urlpatterns = [
    path("api/users/", UserCreateView.as_view(), name="user-create"),
    path("api/users/list/", UserListView.as_view(), name="user-list"),
    path(
        "users/<str:telegram_id>/",
        UserByTelegramView.as_view(),
        name="user-by-telegram_id",
    ),
]
