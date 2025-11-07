"""
Management command to add some electric vehicle test data.
"""
from django.core.management.base import BaseCommand
from marketing.models import CarManufacturer, CarModel, CarVariant


class Command(BaseCommand):
    help = 'Add electric vehicle test data'

    def handle(self, *args, **options):
        # Create Tesla manufacturer if it doesn't exist
        tesla, created = CarManufacturer.objects.get_or_create(
            name="Tesla",
            defaults={'is_active': True}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created manufacturer: {tesla.name}'))

        # Create Nissan if it doesn't exist (for Leaf)
        nissan, created = CarManufacturer.objects.get_or_create(
            name="Nissan", 
            defaults={'is_active': True}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created manufacturer: {nissan.name}'))

        # Create Tesla models
        tesla_models = [
            {"name": "Model S", "body_type": CarModel.BodyType.SEDAN},
            {"name": "Model 3", "body_type": CarModel.BodyType.SEDAN},
            {"name": "Model X", "body_type": CarModel.BodyType.SUV},
            {"name": "Model Y", "body_type": CarModel.BodyType.SUV},
        ]

        for model_data in tesla_models:
            model, created = CarModel.objects.get_or_create(
                manufacturer=tesla,
                name=model_data["name"],
                defaults={
                    'body_type': model_data["body_type"],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created model: {model.manufacturer.name} {model.name}'))

                # Create a variant for each model
                variant = CarVariant.objects.create(
                    model=model,
                    year=2023,
                    trim="Standard",
                    price=45000000,  # 45M Naira
                    transmission=CarVariant.Transmission.AUTOMATIC,
                    listing_type=CarVariant.ListingType.FOREIGN_USED,
                    is_active=True
                )
                self.stdout.write(self.style.SUCCESS(f'Created variant: {variant}'))

        # Create Nissan Leaf
        leaf_model, created = CarModel.objects.get_or_create(
            manufacturer=nissan,
            name="Leaf",
            defaults={
                'body_type': CarModel.BodyType.HATCHBACK,
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created model: {leaf_model.manufacturer.name} {leaf_model.name}'))

            # Create Leaf variant
            leaf_variant = CarVariant.objects.create(
                model=leaf_model,
                year=2022,
                trim="SV",
                price=15000000,  # 15M Naira
                transmission=CarVariant.Transmission.AUTOMATIC,
                listing_type=CarVariant.ListingType.FOREIGN_USED,
                is_active=True
            )
            self.stdout.write(self.style.SUCCESS(f'Created variant: {leaf_variant}'))

        self.stdout.write(self.style.SUCCESS('Successfully added electric vehicle test data!'))