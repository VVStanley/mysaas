from django.contrib.auth import get_user_model
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
)
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from utils.permissions import TokenPermission

from .serializers import UserCreateSerializer, UserSerializer

User = get_user_model()


@extend_schema(
    tags=["Users"],
    summary="Создание нового пользователя",
    description="Регистрация пользователя по Telegram ID. Email не требуется.",
    request=UserSerializer,
    responses={
        201: OpenApiResponse(
            response=UserCreateSerializer,
            description="Пользователь успешно создан",
        ),
        400: OpenApiResponse(
            description="Ошибка валидации",
        ),
    },
    examples=[
        OpenApiExample(
            "Request Example",
            value={"telegram_id": 123456789, "telegram_username": "ivanov_ivan"},
            request_only=True,
        )
    ],
)
class UserCreateView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [TokenPermission]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_serializer = UserSerializer(instance)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@extend_schema(
    tags=["Users"],
    summary="Пользователь по Telegram ID",
    description="Получение пользователя по Telegram ID.",
    responses={
        200: OpenApiResponse(
            response=UserSerializer,
            description="Пользователь получен",
        ),
        404: OpenApiResponse(
            description="Пользователь не найден",
        ),
    },
)
class UserByTelegramView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [TokenPermission]
    lookup_field = "telegram_id"
    lookup_url_kwarg = "telegram_id"


@extend_schema(
    tags=["Users"],
    summary="Все пользователи",
    description="Список пользователей.",
    request=UserSerializer,
    responses={
        200: OpenApiResponse(
            response=UserSerializer,
            description="Пользователи получены",
        )
    },
)
class UserListView(mixins.ListModelMixin, generics.GenericAPIView):
    # ! Нужен?
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [TokenPermission]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
