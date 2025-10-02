from rest_framework import permissions
from django.conf import settings


class TokenPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        auth_header = request.headers.get("Authorization")

        print(request.headers)

        if not auth_header or not auth_header.startswith("Token "):
            return False

        token_key = auth_header.split(" ")[1] if len(auth_header.split(" ")) > 1 else ""
        return token_key == settings.API_TOKEN
