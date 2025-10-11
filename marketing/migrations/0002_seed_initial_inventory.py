from __future__ import annotations

from decimal import Decimal

from django.db import migrations
from django.utils.text import slugify


def unique_slug(model_class, base_slug: str, fallback: str) -> str:
    slug = base_slug or fallback
    counter = 1
    exists = model_class.objects.filter(slug=slug).exists()
    while exists:
        counter += 1
        slug = f"{base_slug}-{counter}" if base_slug else f"{fallback}-{counter}"
        exists = model_class.objects.filter(slug=slug).exists()
    return slug


def seed_initial_inventory(apps, schema_editor):
    Manufacturer = apps.get_model("marketing", "CarManufacturer")
    Model = apps.get_model("marketing", "CarModel")
    Variant = apps.get_model("marketing", "CarVariant")

    inventory = [
        {
            "name": "Toyota",
            "models": [
                {
                    "name": "Corolla",
                    "variants": [
                        {"year": 2024, "price": Decimal("17800000")},
                        {"year": 2023, "price": Decimal("16250000")},
                    ],
                },
                {
                    "name": "RAV4",
                    "variants": [
                        {"year": 2024, "price": Decimal("27850000")},
                        {"year": 2022, "price": Decimal("23800000")},
                    ],
                },
            ],
        },
        {
            "name": "Honda",
            "models": [
                {
                    "name": "Accord",
                    "variants": [
                        {"year": 2023, "price": Decimal("23500000")},
                        {"year": 2021, "price": Decimal("19800000")},
                    ],
                },
                {
                    "name": "CR-V",
                    "variants": [
                        {"year": 2024, "price": Decimal("31200000")},
                        {"year": 2022, "price": Decimal("27950000")},
                    ],
                },
            ],
        },
        {
            "name": "Mercedes-Benz",
            "models": [
                {
                    "name": "C300",
                    "variants": [
                        {"year": 2023, "price": Decimal("38750000")},
                        {"year": 2020, "price": Decimal("32500000")},
                    ],
                },
                {
                    "name": "GLA 250",
                    "variants": [
                        {"year": 2024, "price": Decimal("41500000")},
                        {"year": 2021, "price": Decimal("36200000")},
                    ],
                },
            ],
        },
    ]

    for manufacturer_data in inventory:
        base_manufacturer_slug = slugify(manufacturer_data["name"])
        manufacturer_defaults = {
            "is_active": True,
            "slug": unique_slug(Manufacturer, base_manufacturer_slug, "manufacturer"),
        }
        manufacturer, created = Manufacturer.objects.get_or_create(
            name=manufacturer_data["name"], defaults=manufacturer_defaults
        )
        if not created:
            if not manufacturer.slug:
                manufacturer.slug = unique_slug(Manufacturer, base_manufacturer_slug, "manufacturer")
            manufacturer.is_active = True
            manufacturer.save()

        for model_data in manufacturer_data["models"]:
            base_model_slug = slugify(model_data["name"])
            model_slug = unique_slug(Model, base_model_slug, "model")
            model, created_model = Model.objects.get_or_create(
                manufacturer=manufacturer,
                name=model_data["name"],
                defaults={"is_active": True, "slug": model_slug},
            )
            if not created_model and not model.slug:
                model.slug = unique_slug(Model, base_model_slug, "model")
            model.is_active = True
            model.save()

            for variant_data in model_data["variants"]:
                Variant.objects.update_or_create(
                    model=model,
                    year=variant_data["year"],
                    trim=variant_data.get("trim", ""),
                    defaults={
                        "price": variant_data["price"],
                        "currency": variant_data.get("currency", "NGN"),
                        "is_active": True,
                    },
                )


def unseed_initial_inventory(apps, schema_editor):
    Manufacturer = apps.get_model("marketing", "CarManufacturer")
    Model = apps.get_model("marketing", "CarModel")
    Variant = apps.get_model("marketing", "CarVariant")

    manufacturers = Manufacturer.objects.filter(
        name__in=["Toyota", "Honda", "Mercedes-Benz"]
    )
    Variant.objects.filter(model__manufacturer__in=manufacturers).delete()
    Model.objects.filter(manufacturer__in=manufacturers).delete()
    manufacturers.delete()


class Migration(migrations.Migration):

    dependencies = [
        ("marketing", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_initial_inventory, unseed_initial_inventory),
    ]
