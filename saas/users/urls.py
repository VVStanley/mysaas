from django.urls import path

from .views import (
    UserCreateView,
    UserListView,
    UserRetrieveView,
)

urlpatterns = [
    # Вариант с миксинами
    path("api/users/", UserCreateView.as_view(), name="user-create"),
    path("api/users/me/", UserRetrieveView.as_view(), name="user-me"),
    path("api/users/list/", UserListView.as_view(), name="user-list"),
]
