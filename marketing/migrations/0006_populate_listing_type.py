from django.db import migrations


def assign_listing_types(apps, schema_editor):
    CarVariant = apps.get_model("marketing", "CarVariant")

    for variant in CarVariant.objects.all():
        if variant.year >= 2023:
            variant.listing_type = "foreign-used"
        else:
            variant.listing_type = "registered"
        variant.save(update_fields=["listing_type"])


def unassign_listing_types(apps, schema_editor):
    CarVariant = apps.get_model("marketing", "CarVariant")
    CarVariant.objects.update(listing_type="registered")


class Migration(migrations.Migration):

    dependencies = [
        ("marketing", "0005_carvariant_listing_type"),
    ]

    operations = [
        migrations.RunPython(assign_listing_types, unassign_listing_types),
    ]
