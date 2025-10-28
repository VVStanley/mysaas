from django.db import migrations


def create_initial_tariffs(apps, schema_editor):
    Tariff = apps.get_model("tariff", "Tariff")
    TariffLimit = apps.get_model("tariff", "TariffLimit")

    all_limits = TariffLimit.objects.create(
        code="all",
        max_ai_generations=5,
        max_products=5,
    )

    tariffs_data = [
        {
            "code": "free",
            "price": 0,
            "description": "Бесплатный тариф с базовыми возможностями",
            "order": 1,
            "limits": all_limits,
        },
        {
            "code": "basic",
            "price": 190,
            "description": "Базовый тариф для серьезной работы",
            "order": 2,
            "limits": all_limits,
        },
        {
            "code": "premium",
            "price": 390,
            "description": "Премиум тариф с максимальными возможностями",
            "order": 3,
            "limits": all_limits,
        },
    ]

    for tariff_data in tariffs_data:
        Tariff.objects.get_or_create(code=tariff_data["code"], defaults=tariff_data)


def reverse_migration(apps, schema_editor):
    Tariff = apps.get_model("tariff", "Tariff")
    TariffLimit = apps.get_model("tariff", "TariffLimit")
    Tariff.objects.all().delete()
    TariffLimit.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("tariff", "0002_alter_tarifflimit_code"),
    ]

    operations = [
        migrations.RunPython(create_initial_tariffs, reverse_migration),
    ]
