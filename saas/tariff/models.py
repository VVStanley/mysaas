from django.db import models


class TariffCode(models.TextChoices):
    FREE = "free", "Бесплатный"
    BASIC = "basic", "Базовый"
    PREMIUM = "premium", "Премиум"


class MarketplaceCode(models.TextChoices):
    ALL = "all", "all"
    WB = "wb", "Wildberries"
    OZON = "ozon", "Ozon"
    YANDEX_MARKET = "yandex_market", "Яндекс Маркет"
    ALIEXPRESS = "aliexpress", "AliExpress"


class TariffLimit(models.Model):
    code = models.CharField(
        max_length=50,
        unique=True,
        default=MarketplaceCode.ALL,
        choices=MarketplaceCode.choices,
        verbose_name="Код маркетплейса",
    )
    max_ai_generations = models.PositiveIntegerField(
        default=50, verbose_name="Макс. генераций ИИ в месяц"
    )
    max_products = models.PositiveIntegerField(
        default=100, verbose_name="Макс. товаров для отслеживания"
    )

    class Meta:
        db_table = "tariff_limits"
        verbose_name = "Маркетплейс"
        verbose_name_plural = "Маркетплейсы"

    def __str__(self):
        return self.get_code_display()


class Tariff(models.Model):
    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Код тарифа",
        choices=TariffCode.choices,
    )
    limits = models.ForeignKey(
        TariffLimit,
        on_delete=models.PROTECT,
        verbose_name="Tariff limits",
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Цена в месяц (руб)"
    )
    description = models.TextField(blank=True, verbose_name="Описание")
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок отображения")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tariffs"
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"
        ordering = ["order", "price"]

    def __str__(self):
        return f"{self.name} ({self.price} руб/мес)"
