from django.contrib.auth import get_user_model
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
)
from rest_framework import generics, mixins, status
from utils.permissions import TokenPermission
from rest_framework.response import Response
from .serializers import UserCreateSerializer, UserSerializer

User = get_user_model()


@extend_schema(
    tags=["Users"],
    summary="Создание нового пользователя",
    description="Регистрация пользователя по Telegram ID. Email не требуется.",
    request=UserCreateSerializer,
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
    """
    Создание пользователя через миксины
    """

    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [TokenPermission]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        # Дополнительная логика при создании пользователя
        user = serializer.save()
        # Здесь можно добавить отправку welcome сообщения и т.д.

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Кастомный ответ
        return Response(
            {"message": "Пользователь успешно создан", "data": serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


@extend_schema(
    tags=["Users"],
    summary="Пользователь",
    description="ПОльзователь.",
    request=UserSerializer,
    responses={
        200: OpenApiResponse(
            response=UserSerializer,
            description="Пользователь получен",
        ),
        404: OpenApiResponse(
            description="ПОльзователь не найден",
        ),
    },
)
class UserRetrieveView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """
    Получение информации о пользователе
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [TokenPermission]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def get_object(self):
        # Возвращаем текущего пользователя
        return self.request.user


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
    """
    Список пользователей (только для админов)
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [TokenPermission]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        # Только суперпользователи могут видеть всех пользователей
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)
