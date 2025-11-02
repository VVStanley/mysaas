from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from tariff.models import Tariff, TariffCode


def _get_tariff_default():
    try:
        return Tariff.objects.get(code=TariffCode.FREE).id
    except Tariff.DoesNotExist:
        return None


class UserManager(BaseUserManager):
    def create_user(self, telegram_id: int, password=None, **extra_fields):
        if not telegram_id:
            raise ValueError("The Telegram ID must be set")
        user = self.model(telegram_id=telegram_id, **extra_fields)
        if not password:
            password = get_random_string(length=12)
        user.save(using=self._db)
        return user

    def create_superuser(self, telegram_id, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(telegram_id, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    telegram_id = models.BigIntegerField(unique=True, verbose_name="Telegram ID")
    telegram_username = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Telegram ник"
    )
    tariff = models.ForeignKey(
        Tariff,
        on_delete=models.PROTECT,
        default=_get_tariff_default,
        verbose_name="Тариф",
        related_name="users",
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    USERNAME_FIELD = "telegram_id"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        db_table = "users"

    def __str__(self):
        return f"tg:{self.telegram_id} ({self.telegram_username or 'no name'})"
