from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    telegram_id = serializers.IntegerField(required=True)
    telegram_username = serializers.CharField(
        required=False, allow_blank=True, allow_null=True, trim_whitespace=False
    )

    class Meta:
        model = User
        fields = ("telegram_id", "telegram_username", "tariff")
        read_only_fields = ("tariff",)

    def validate_telegram_id(self, value):
        if User.objects.filter(telegram_id=value).exists():
            raise serializers.ValidationError("Пользователь с таким Telegram ID уже существует.")
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "telegram_id", "telegram_username", "tariff", "date_joined")
        read_only_fields = fields
