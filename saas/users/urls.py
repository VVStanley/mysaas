from django.urls import path

from .views import (
    UserByTelegramView,
    UserCreateView,
    UserListView,
)

urlpatterns = [
    path("", UserCreateView.as_view(), name="user-create"),
    path("list/", UserListView.as_view(), name="user-list"),
    path(
        "<str:telegram_id>/",
        UserByTelegramView.as_view(),
        name="user-by-telegram_id",
    ),
]
