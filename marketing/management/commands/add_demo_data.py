from __future__ import annotations

from django.core.management.base import BaseCommand
from django.db import transaction

from marketing.models import (
	CarManufacturer,
	CarModel,
	CarVariant,
	CarVariantDetail,
	CarVariantFeature,
	CarVariantImage,
	CarVariantSpecification,
	HomepageFeaturedVehicle,
)


class Command(BaseCommand):
	help = "Add more demo data to the database for testing and demonstration."

	@transaction.atomic
	def handle(self, *args, **options):
		self.stdout.write("Adding more demo data...")
		self._create_manufacturers_and_models()
		self._create_variants()
		self._create_featured_vehicles()
		self.stdout.write(self.style.SUCCESS("Demo data added successfully."))

	def _create_manufacturers_and_models(self):
		# Toyota models
		toyota, _ = CarManufacturer.objects.get_or_create(
			name="Toyota",
			defaults={"slug": "toyota", "is_active": True}
		)
		
		models_data = [
			("Camry", CarModel.BodyType.SEDAN),
			("Prius", CarModel.BodyType.SEDAN),
			("Highlander", CarModel.BodyType.SUV),
			("Sienna", CarModel.BodyType.SUV),
			("Tacoma", CarModel.BodyType.TRUCK),
		]
		
		for model_name, body_type in models_data:
			CarModel.objects.get_or_create(
				manufacturer=toyota,
				name=model_name,
				defaults={"slug": model_name.lower(), "body_type": body_type, "is_active": True}
			)

		# Honda models
		honda, _ = CarManufacturer.objects.get_or_create(
			name="Honda",
			defaults={"slug": "honda", "is_active": True}
		)
		
		honda_models = [
			("Civic", CarModel.BodyType.SEDAN),
			("Pilot", CarModel.BodyType.SUV),
			("Ridgeline", CarModel.BodyType.TRUCK),
			("Odyssey", CarModel.BodyType.SUV),
		]
		
		for model_name, body_type in honda_models:
			CarModel.objects.get_or_create(
				manufacturer=honda,
				name=model_name,
				defaults={"slug": model_name.lower(), "body_type": body_type, "is_active": True}
			)

		# Nissan
		nissan, _ = CarManufacturer.objects.get_or_create(
			name="Nissan",
			defaults={"slug": "nissan", "is_active": True}
		)
		
		nissan_models = [
			("Altima", CarModel.BodyType.SEDAN),
			("Sentra", CarModel.BodyType.SEDAN),
			("Murano", CarModel.BodyType.SUV),
			("Pathfinder", CarModel.BodyType.SUV),
			("Rogue", CarModel.BodyType.SUV),
			("Frontier", CarModel.BodyType.TRUCK),
		]
		
		for model_name, body_type in nissan_models:
			CarModel.objects.get_or_create(
				manufacturer=nissan,
				name=model_name,
				defaults={"slug": model_name.lower(), "body_type": body_type, "is_active": True}
			)

		# Ford
		ford, _ = CarManufacturer.objects.get_or_create(
			name="Ford",
			defaults={"slug": "ford", "is_active": True}
		)
		
		ford_models = [
			("Fusion", CarModel.BodyType.SEDAN),
			("Explorer", CarModel.BodyType.SUV),
			("Escape", CarModel.BodyType.SUV),
			("F-150", CarModel.BodyType.TRUCK),
			("Edge", CarModel.BodyType.SUV),
		]
		
		for model_name, body_type in ford_models:
			CarModel.objects.get_or_create(
				manufacturer=ford,
				name=model_name,
				defaults={"slug": model_name.lower(), "body_type": body_type, "is_active": True}
			)

		# BMW
		bmw, _ = CarManufacturer.objects.get_or_create(
			name="BMW",
			defaults={"slug": "bmw", "is_active": True}
		)
		
		bmw_models = [
			("3 Series", CarModel.BodyType.SEDAN),
			("5 Series", CarModel.BodyType.SEDAN),
			("X3", CarModel.BodyType.SUV),
			("X5", CarModel.BodyType.SUV),
			("7 Series", CarModel.BodyType.SEDAN),
		]
		
		for model_name, body_type in bmw_models:
			CarModel.objects.get_or_create(
				manufacturer=bmw,
				name=model_name,
				defaults={"slug": model_name.lower().replace(" ", "-"), "body_type": body_type, "is_active": True}
			)

		# Audi
		audi, _ = CarManufacturer.objects.get_or_create(
			name="Audi",
			defaults={"slug": "audi", "is_active": True}
		)
		
		audi_models = [
			("A4", CarModel.BodyType.SEDAN),
			("A6", CarModel.BodyType.SEDAN),
			("Q5", CarModel.BodyType.SUV),
			("Q7", CarModel.BodyType.SUV),
			("A3", CarModel.BodyType.SEDAN),
		]
		
		for model_name, body_type in audi_models:
			CarModel.objects.get_or_create(
				manufacturer=audi,
				name=model_name,
				defaults={"slug": model_name.lower(), "body_type": body_type, "is_active": True}
			)

	def _create_variants(self):
		# Get all models and create variants for each
		models = CarModel.objects.filter(is_active=True)
		
		years = [2024, 2023, 2022, 2021, 2020, 2019]
		trims = ["Base", "Sport", "Limited", "Premium", "SE", "EX", "LX"]
		transmissions = [CarVariant.Transmission.AUTOMATIC, CarVariant.Transmission.MANUAL]
		listing_types = [CarVariant.ListingType.REGISTERED, CarVariant.ListingType.FOREIGN_USED]
		
		variant_count = 0
		for model in models:
			for year in years[:3]:  # Only create variants for recent years to keep it manageable
				for trim in trims[:2]:  # Only create 2 trims per model/year
					if variant_count >= 50:  # Limit total variants
						break
					
					# Calculate price based on brand, year, and model type
					base_price = self._calculate_base_price(model, year)
					
					variant, created = CarVariant.objects.get_or_create(
						model=model,
						year=year,
						trim=trim,
						defaults={
							"price": str(base_price),
							"transmission": transmissions[variant_count % 2],
							"listing_type": listing_types[variant_count % 2],
							"currency": "NGN",
							"is_active": True,
						}
					)
					
					if created:
						variant_count += 1
						self._create_variant_details(variant)
				
				if variant_count >= 50:
					break
			
			if variant_count >= 50:
				break

	def _calculate_base_price(self, model, year):
		"""Calculate base price based on manufacturer, model type, and year"""
		base_prices = {
			"Toyota": {"SEDAN": 15000000, "SUV": 25000000, "TRUCK": 30000000},
			"Honda": {"SEDAN": 14000000, "SUV": 23000000, "TRUCK": 28000000},
			"Nissan": {"SEDAN": 12000000, "SUV": 20000000, "TRUCK": 25000000},
			"Ford": {"SEDAN": 13000000, "SUV": 22000000, "TRUCK": 32000000},
			"BMW": {"SEDAN": 35000000, "SUV": 45000000, "TRUCK": 50000000},
			"Mercedes-Benz": {"SEDAN": 40000000, "SUV": 50000000, "TRUCK": 55000000},
			"Audi": {"SEDAN": 32000000, "SUV": 42000000, "TRUCK": 47000000},
		}
		
		manufacturer_prices = base_prices.get(model.manufacturer.name, {"SEDAN": 15000000, "SUV": 25000000, "TRUCK": 30000000})
		base_price = manufacturer_prices.get(model.body_type, 15000000)
		
		# Adjust for year (newer cars cost more)
		year_multiplier = 1 + (year - 2019) * 0.1
		
		return int(base_price * year_multiplier)

	def _create_variant_details(self, variant):
		"""Create detailed information for a variant"""
		# Create variant detail
		mileage_km = max((2024 - variant.year) * 15000 + (hash(variant.trim) % 20000), 5000)
		
		locations = ["Lagos, Nigeria", "Abuja, Nigeria", "Port Harcourt, Nigeria", "Ibadan, Nigeria", "Kano, Nigeria"]
		
		CarVariantDetail.objects.get_or_create(
			variant=variant,
			defaults={
				"headline": f"{variant.model.manufacturer.name} {variant.model.name} - Premium Choice",
				"subheadline": f"Certified {variant.year} {variant.model.name} with verified history.",
				"description": f"This {variant.year} {variant.model.manufacturer.name} {variant.model.name} {variant.trim} offers exceptional reliability and performance. Thoroughly inspected by Todde engineers with full documentation.",
				"mileage_km": mileage_km,
				"location": locations[hash(variant.trim) % len(locations)],
				"finance_intro": "Flexible financing options available with competitive rates.",
				"loan_rate": "17.5",
				"loan_deposit_percent": "30",
				"loan_period_months": 24,
				"applicant_types": "Salary earner, Business owner, Ride-hailing partner",
				"is_active": True,
			}
		)
		
		# Create variant images
		image_urls = [
			"https://images.unsplash.com/photo-1494976388531-d1058494cdd8?auto=format&fit=crop&w=1600&q=80",
			"https://images.unsplash.com/photo-1549924231-f129b911e442?auto=format&fit=crop&w=1600&q=80",
			"https://images.unsplash.com/photo-1549921296-3b4a6b789555?auto=format&fit=crop&w=1600&q=80",
			"https://images.unsplash.com/photo-1503736334956-4c8f8e92946d?auto=format&fit=crop&w=1600&q=80",
			"https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?auto=format&fit=crop&w=1600&q=80",
		]
		
		for i, url in enumerate(image_urls[:3], 1):
			CarVariantImage.objects.get_or_create(
				variant=variant,
				order=i,
				defaults={
					"image_url": url,
					"alt_text": f"{variant.model.manufacturer.name} {variant.model.name} {variant.year}",
					"is_active": True,
				}
			)
		
		# Create variant features
		common_features = [
			"Air conditioning",
			"Power steering",
			"Anti-lock braking system",
			"Airbag system",
			"Central locking",
			"Electric windows",
			"Touchscreen infotainment",
			"Bluetooth connectivity",
			"Reverse camera",
			"Alloy wheels",
		]
		
		# Select random features based on trim level
		num_features = 6 if variant.trim in ["Premium", "Limited"] else 4
		selected_features = common_features[:num_features]
		
		for i, feature in enumerate(selected_features, 1):
			CarVariantFeature.objects.get_or_create(
				variant=variant,
				order=i,
				defaults={
					"text": feature,
					"is_active": True,
				}
			)
		
		# Create specifications
		specs = [
			("Engine Type", "4-Cylinder Turbo"),
			("Fuel Type", "Petrol"),
			("Transmission", variant.get_transmission_display()),
			("Mileage", f"{mileage_km:,} km"),
			("Body Type", variant.model.get_body_type_display()),
			("Year", str(variant.year)),
			("Color", "Various Available"),
		]
		
		for i, (label, value) in enumerate(specs, 1):
			CarVariantSpecification.objects.get_or_create(
				variant=variant,
				order=i,
				defaults={
					"label": label,
					"value": value,
					"is_active": True,
				}
			)

	def _create_featured_vehicles(self):
		"""Create additional featured vehicles"""
		variants = CarVariant.objects.filter(is_active=True)[:10]
		
		featured_data = [
			{"badge": "Best Value", "name": "2024 Toyota Camry SE"},
			{"badge": "Popular Choice", "name": "2023 Honda Civic Sport"},
			{"badge": "New Arrival", "name": "2024 Nissan Altima Premium"},
			{"badge": "Top Rated", "name": "2023 BMW 3 Series"},
			{"badge": "Family Favorite", "name": "2024 Toyota Highlander"},
			{"badge": "Luxury Pick", "name": "2023 Mercedes-Benz C300"},
			{"badge": "Efficient Choice", "name": "2024 Toyota Prius Limited"},
			{"badge": "Adventure Ready", "name": "2023 Ford Explorer Sport"},
		]
		
		locations = ["Lagos, Nigeria", "Abuja, Nigeria", "Port Harcourt, Nigeria", "Ibadan, Nigeria"]
		image_urls = [
			"https://images.unsplash.com/photo-1549921296-3b4a6b789555?auto=format&fit=crop&w=800&q=80",
			"https://images.unsplash.com/photo-1563720223185-11003d516935?auto=format&fit=crop&w=800&q=80",
			"https://images.unsplash.com/photo-1494976388531-d1058494cdd8?auto=format&fit=crop&w=800&q=80",
			"https://images.unsplash.com/photo-1517677129300-07b130802f46?auto=format&fit=crop&w=800&q=80",
			"https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?auto=format&fit=crop&w=800&q=80",
		]
		
		# Only create if we don't have many featured vehicles already
		existing_count = HomepageFeaturedVehicle.objects.filter(is_active=True).count()
		
		for i, (variant, data) in enumerate(zip(variants, featured_data), start=existing_count + 1):
			if i > 12:  # Limit total featured vehicles
				break
				
			HomepageFeaturedVehicle.objects.get_or_create(
				order=i,
				defaults={
					"variant": variant,
					"name": data["name"],
					"badge": data["badge"],
					"location": locations[i % len(locations)],
					"image_url": image_urls[i % len(image_urls)],
					"price": f"₦{variant.price:,}" if variant.price else "",
					"payment_plan": f"₦{int(float(variant.price) * 0.3):,} down • ₦{int(float(variant.price) * 0.7 / 24):,} / month" if variant.price else "",
					"is_active": True,
				}
			)