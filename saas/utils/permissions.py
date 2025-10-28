from django.conf import settings
from rest_framework import permissions


class TokenPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        token_key = request.headers.get("Authorization")
        return token_key == settings.API_TOKEN if token_key else False
