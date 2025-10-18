from __future__ import annotations

from django.db import migrations


def populate_vehicle_metadata(apps, schema_editor):
    CarModel = apps.get_model("marketing", "CarModel")
    CarVariant = apps.get_model("marketing", "CarVariant")

    body_type_map = {
        "corolla": "sedan",
        "rav4": "suv",
        "accord": "sedan",
        "cr-v": "suv",
        "c300": "sedan",
        "gla": "suv",
    }

    for model in CarModel.objects.all():
        name_key = model.name.lower()
        body_type = "sedan"
        for key, mapped_body in body_type_map.items():
            if key in name_key:
                body_type = mapped_body
                break
        model.body_type = body_type
        model.save(update_fields=["body_type"])

    for variant in CarVariant.objects.all():
        if variant.year <= 2021:
            transmission = "manual"
        elif variant.model.name.lower() in {"corolla", "accord"}:
            transmission = "cvt"
        else:
            transmission = "automatic"
        variant.transmission = transmission
        variant.save(update_fields=["transmission"])


def unpopulate_vehicle_metadata(apps, schema_editor):
    CarModel = apps.get_model("marketing", "CarModel")
    CarVariant = apps.get_model("marketing", "CarVariant")

    CarModel.objects.update(body_type="sedan")
    CarVariant.objects.update(transmission="automatic")


class Migration(migrations.Migration):

    dependencies = [
        ("marketing", "0003_carmodel_body_type_carvariant_transmission"),
    ]

    operations = [
        migrations.RunPython(populate_vehicle_metadata, unpopulate_vehicle_metadata),
    ]
