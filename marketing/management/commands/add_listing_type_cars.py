"""
Management command to add some listing type test data.
"""
from django.core.management.base import BaseCommand
from marketing.models import CarManufacturer, CarModel, CarVariant


class Command(BaseCommand):
    help = 'Add listing type test data for foreign used and registered cars'

    def handle(self, *args, **options):
        # Get existing manufacturers
        toyota = CarManufacturer.objects.filter(name="Toyota").first()
        honda = CarManufacturer.objects.filter(name="Honda").first()
        
        # Create manufacturers if they don't exist
        if not toyota:
            toyota = CarManufacturer.objects.create(name="Toyota", is_active=True)
            self.stdout.write(self.style.SUCCESS(f'Created manufacturer: {toyota.name}'))
        
        if not honda:
            honda = CarManufacturer.objects.create(name="Honda", is_active=True)
            self.stdout.write(self.style.SUCCESS(f'Created manufacturer: {honda.name}'))

        # Create some Toyota models
        camry_model, created = CarModel.objects.get_or_create(
            manufacturer=toyota,
            name="Camry",
            defaults={
                'body_type': CarModel.BodyType.SEDAN,
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created model: {camry_model.manufacturer.name} {camry_model.name}'))

        # Create some Honda models  
        accord_model, created = CarModel.objects.get_or_create(
            manufacturer=honda,
            name="Accord",
            defaults={
                'body_type': CarModel.BodyType.SEDAN,
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created model: {accord_model.manufacturer.name} {accord_model.name}'))

        # Create Foreign Used variants
        foreign_used_cars = [
            {
                "model": camry_model,
                "year": 2020,
                "trim": "LE",
                "price": 25000000,  # 25M Naira
                "listing_type": CarVariant.ListingType.FOREIGN_USED
            },
            {
                "model": accord_model,
                "year": 2019,
                "trim": "Sport",
                "price": 23000000,  # 23M Naira
                "listing_type": CarVariant.ListingType.FOREIGN_USED
            },
        ]

        # Create Registered (Nigerian Used) variants
        registered_cars = [
            {
                "model": camry_model,
                "year": 2018,
                "trim": "XLE",
                "price": 18000000,  # 18M Naira
                "listing_type": CarVariant.ListingType.REGISTERED
            },
            {
                "model": accord_model,
                "year": 2017,
                "trim": "EX-L",
                "price": 16000000,  # 16M Naira
                "listing_type": CarVariant.ListingType.REGISTERED
            },
        ]

        # Create all variants
        all_cars = foreign_used_cars + registered_cars
        
        for car_data in all_cars:
            variant, created = CarVariant.objects.get_or_create(
                model=car_data["model"],
                year=car_data["year"],
                trim=car_data["trim"],
                defaults={
                    'price': car_data["price"],
                    'transmission': CarVariant.Transmission.AUTOMATIC,
                    'listing_type': car_data["listing_type"],
                    'is_active': True
                }
            )
            if created:
                listing_type_display = "Foreign Used" if car_data["listing_type"] == CarVariant.ListingType.FOREIGN_USED else "Nigerian Used"
                self.stdout.write(self.style.SUCCESS(f'Created {listing_type_display} variant: {variant}'))

        self.stdout.write(self.style.SUCCESS('Successfully added listing type test data!'))