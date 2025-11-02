from django.contrib.auth import get_user_model
from rest_framework import serializers
from tariff.models import Tariff, TariffCode

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    telegram_id = serializers.IntegerField(required=True)
    telegram_username = serializers.CharField(
        required=False, allow_blank=True, allow_null=True, trim_whitespace=False
    )

    class Meta:
        model = User
        fields = ("telegram_id", "telegram_username")

    def validate_telegram_id(self, value):
        if User.objects.filter(telegram_id=value).exists():
            raise serializers.ValidationError(
                "Пользователь с таким Telegram ID уже существует."
            )
        return value


class TariffSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    code = serializers.ChoiceField(choices=TariffCode.choices)

    def get_name(self, obj):
        return obj.get_code_display()

    class Meta:
        model = Tariff
        fields = ("id", "code", "name", "price", "description")
        read_only_fields = fields


class UserSerializer(serializers.ModelSerializer):
    tariff = TariffSerializer(read_only=True)

    class Meta:
        model = User
        fields = ("telegram_id", "telegram_username", "tariff", "date_joined")
        read_only_fields = fields
