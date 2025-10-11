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
	FinancingBenefit,
	FinancingPageConfig,
	FinancingSnapshotItem,
	HomepageBrandMetric,
	HomepageCategory,
	HomepageContactCard,
	HomepageFeaturedVehicle,
	HomepageFinancingHighlight,
	HomepageFinancingStep,
	HomepageHero,
	HomepageSectionCopy,
	HomepageValueProposition,
	InventoryPageConfig,
	NavigationLink,
)


class Command(BaseCommand):
	help = "Seed homepage content and sample inventory data for Todde."

	@transaction.atomic
	def handle(self, *args, **options):
		self.stdout.write("Seeding homepage content…")
		self._seed_navigation()
		self._seed_copy()
		self._seed_inventory_configs()
		self._seed_hero()
		self._seed_categories()
		self._seed_value_props()
		self._seed_brand_metrics()
		self._seed_financing_highlights()
		self._seed_financing_steps()
		self._seed_financing_page_config()
		self._seed_financing_snapshot()
		self._seed_financing_benefits()
		self._seed_contact_cards()
		variant = self._ensure_sample_inventory()
		self._seed_featured_vehicles(variant)
		self._seed_variant_details()
		self.stdout.write(self.style.SUCCESS("Homepage content seeded successfully."))

	def _seed_navigation(self) -> None:
		links = [
			{"label": "Registered Cars", "href": "/registered-cars/", "description": "Browse locally registered inventory", "order": 1},
			{"label": "Foreign Used", "href": "/foreign-used/", "description": "Tokunbo vehicles ready to import", "order": 2},
			{"label": "All Cars", "href": "/cars/", "description": "Entire Todde marketplace", "order": 3},
			{"label": "Car Finance", "href": "/financing/", "description": "Explore financing plans", "order": 4},
		]
		for item in links:
			NavigationLink.objects.update_or_create(
				label=item["label"],
				defaults={
					"href": item["href"],
					"description": item["description"],
					"order": item["order"],
					"is_active": True,
				},
			)

	def _seed_copy(self) -> None:
		entries = {
			"meta": {
				"heading": "Todde Integrated Services | Empowering Nigerians to own cars with flexible financing",
				"subheading": "Shop certified vehicles, access Todde's flexible financing, and drive home with confidence in 48 hours.",
			},
			"categories": {
				"heading": "Browse by category",
				"subheading": "Find the perfect car for work, family, or adventure.",
				"cta_label": "Schedule a test drive",
				"cta_url": "/financing/",
			},
			"featured": {
				"heading": "Featured vehicles",
				"subheading": "Handpicked cars, verified by Todde engineers.",
				"cta_label": "Start financing",
				"cta_url": "/financing/",
			},
			"value_props": {
				"heading": "Why choose Todde?",
				"subheading": "A full-stack automotive partner that delivers value before and after you take the keys.",
			},
			"financing_cta": {
				"heading": "Unlock Todde Financing",
				"subheading": "Spread payments up to 36 months, enjoy bundled insurance, and stay road-ready with maintenance support.",
				"supporting_text": "Decisions within 48 hours • Powered by Todde partner banks",
				"cta_label": "Learn more",
				"cta_url": "/financing/",
			},
			"contact": {
				"heading": "Ready to get started?",
				"subheading": "Schedule a consultation with a Todde advisor to explore inventory, financing, and partner perks.",
			},
			"financing_meta": {
				"heading": "Todde Car Financing | Spread payments and own your dream car",
				"subheading": "Pay only 30% upfront and finance the rest with Todde. See how our 8-step process gets you on the road fast.",
			},
		}
		for slug, defaults in entries.items():
			HomepageSectionCopy.objects.update_or_create(
				slug=slug,
				defaults={
					**defaults,
					"is_active": True,
				},
			)

	def _seed_hero(self) -> None:
		hero_defaults = {
			"badge_label": "Todde Marketplace",
			"title": "Auto Financing That Gets You On The Road Faster",
			"subtitle": "Discover certified vehicles, compare transparent repayment plans, and secure Todde financing with as little as 30% upfront.",
			"primary_cta_label": "Discover more",
			"primary_cta_url": "/financing/",
			"image_url": "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?auto=format&fit=crop&w=1600&q=80",
			"order": 1,
			"is_active": True,
		}
		HomepageHero.objects.update_or_create(order=1, defaults=hero_defaults)

	def _seed_categories(self) -> None:
		categories = [
			("Sedans", "heroicons:car", "Comfortable daily drivers"),
			("SUVs", "heroicons:truck", "Spacious family rides"),
			("Electric", "heroicons:bolt", "Energy-efficient innovation"),
			("Luxury", "heroicons:sparkles", "Premium experiences"),
		]
		for index, (name, icon, description) in enumerate(categories, start=1):
			HomepageCategory.objects.update_or_create(
				name=name,
				defaults={
					"icon": icon,
					"description": description,
					"order": index,
					"is_active": True,
				},
			)

	def _seed_value_props(self) -> None:
		value_props = [
			("Certified Quality", "Every vehicle passes a 200-point inspection with transparent history reports.", "heroicons:shield-check"),
			("Smart Pricing", "We leverage market data and partner network to deliver unmatched deals.", "heroicons:banknotes"),
			("Always-On Support", "Dedicated advisors guide you through selection, financing, and ownership.", "heroicons:lifebuoy"),
			("Flexible Financing", "Pay only 30% upfront and spread the balance over up to 36 months.", "heroicons:sparkles"),
		]
		for index, (title, description, icon) in enumerate(value_props, start=1):
			HomepageValueProposition.objects.update_or_create(
				title=title,
				defaults={
					"description": description,
					"icon": icon,
					"order": index,
					"is_active": True,
				},
			)

	def _seed_brand_metrics(self) -> None:
		metrics = [
			("15K+", "Customers empowered"),
			("300+", "Cars financed this year"),
			("48hrs", "Average approval time"),
		]
		for index, (value, label) in enumerate(metrics, start=1):
			HomepageBrandMetric.objects.update_or_create(
				value=value,
				defaults={
					"label": label,
					"order": index,
					"is_active": True,
				},
			)

	def _seed_financing_highlights(self) -> None:
		highlights = [
			("Up to 36 months", "Flexible tenors that match your income cycle."),
			("Low interest rates", "Negotiated rates through Todde financial partners."),
			("Insurance & maintenance", "Bundled coverage keeps you protected on the road."),
		]
		for index, (title, description) in enumerate(highlights, start=1):
			HomepageFinancingHighlight.objects.update_or_create(
				title=title,
				defaults={
					"description": description,
					"order": index,
					"is_active": True,
				},
			)

	def _seed_financing_steps(self) -> None:
		steps = [
			("Create your Todde account", "Start with your BVN and contact details."),
			("Choose your vehicle", "Browse inspected inventory or request custom sourcing."),
			("Submit quick application", "Provide employment, income, and preferred repayment tenor."),
			("Get instant decision", "Receive a tailored repayment plan in under 24 hours."),
			("Pay 30% deposit", "Secure your car with Todde's low upfront commitment."),
			("Drive home", "Pick-up from a Todde hub or request doorstep delivery."),
			("Make monthly payments", "Automated reminders and flexible payment channels."),
			("Own it outright", "Complete your instalments and receive your ownership certificate."),
		]
		for index, (title, description) in enumerate(steps, start=1):
			HomepageFinancingStep.objects.update_or_create(
				title=title,
				defaults={
					"description": description,
					"order": index,
					"is_active": True,
				},
			)

	def _seed_financing_page_config(self) -> None:
		FinancingPageConfig.objects.update_or_create(
			slug=FinancingPageConfig.Slug.DEFAULT,
			defaults={
				"hero_title": "Buy your dream car, now. Pay monthly.",
				"hero_subtitle": "Todde Financing makes car ownership accessible with transparent offers, fair interest rates, and bundled protection.",
				"hero_primary_cta_label": "Start now",
				"hero_primary_cta_url": "/financing/",
				"hero_secondary_cta_label": "Explore inventory",
				"hero_secondary_cta_url": "/#inventory",
				"hero_background_image_url": "https://images.unsplash.com/photo-1517677129300-07b130802f46?auto=format&fit=crop&w=1400&q=80",
				"hero_callout_title": "Need advice?",
				"hero_callout_text": "Book a free financing clinic every Friday at Todde hubs nationwide.",
				"steps_heading": "How Todde Financing works",
				"steps_subheading": "Eight clear steps to owning your vehicle with confidence.",
				"benefits_heading": "What you get with every plan",
				"benefits_subheading": "",
				"eligibility_heading": "Eligibility snapshot",
				"eligibility_description": "Minimum monthly income of ₦250,000, verifiable employment, and BVN confirmation.",
				"eligibility_cta_label": "Review full requirements",
				"eligibility_cta_url": "/financing/",
				"testimonial_image_url": "https://images.unsplash.com/photo-1502877338535-766e1452684a?auto=format&fit=crop&w=900&q=80",
				"testimonial_card_title": "Todde customer stories",
				"testimonial_card_text": "“Financing with Todde helped our logistics business scale in 3 months.”",
				"corporate_heading": "Bring Todde Financing to your business fleets",
				"corporate_subheading": "Talk to us about flexible corporate plans, driver training, and maintenance coordination.",
				"corporate_primary_cta_label": "Partner with Todde",
				"corporate_primary_cta_url": "mailto:partners@todde.africa",
				"corporate_secondary_cta_label": "Call +234 1700 1234",
				"corporate_secondary_cta_url": "tel:+23417001234",
				"corporate_availability_heading": "Available nationwide",
				"corporate_availability_description": "Lagos • Abuja • Port Harcourt • Ibadan • Enugu",
				"is_active": True,
			},
		)

	def _seed_financing_snapshot(self) -> None:
		items = [
			"Pay only 30% upfront and get your keys within 48 hours of approval.",
			"Automated payment reminders and flexible repayment channels.",
			"Roadside assistance, insurance, and maintenance bundles included.",
		]
		for index, text in enumerate(items, start=1):
			FinancingSnapshotItem.objects.update_or_create(
				order=index,
				defaults={
					"text": text,
					"is_active": True,
				},
			)

	def _seed_financing_benefits(self) -> None:
		benefits = [
			("Comprehensive insurance", "Comprehensive insurance coverage and annual renewals handled by Todde.", "heroicons:shield-check"),
			("Dedicated support", "Dedicated support agents for servicing, documentation, and payment plans.", "heroicons:lifebuoy"),
			("Transparent pricing", "Transparent pricing and zero hidden charges on every contract.", "heroicons:banknotes"),
		]
		for index, (title, description, icon) in enumerate(benefits, start=1):
			FinancingBenefit.objects.update_or_create(
				title=title,
				defaults={
					"description": description,
					"icon": icon,
					"order": index,
					"is_active": True,
				},
			)

	def _seed_contact_cards(self) -> None:
		cards = [
			("Visit us", "Plot 24, Admiralty Road, Lekki Phase 1, Lagos.", "", ""),
			("Support", "Talk to us on WhatsApp:", "+234 701 001 2345", "https://wa.me/2347010012345"),
		]
		for index, (title, description, link_label, link_url) in enumerate(cards, start=1):
			HomepageContactCard.objects.update_or_create(
				title=title,
				defaults={
					"description": description,
					"link_label": link_label,
					"link_url": link_url,
					"order": index,
					"is_active": True,
				},
			)

	def _seed_inventory_configs(self) -> None:
		configs = [
			{
				"slug": InventoryPageConfig.Slug.ALL,
				"listing_type": "",
				"title": "All Cars",
				"intro_text": "Discover certified cars inspected by Todde. Use the filters to zero in on the right price, year, transmission, or body style.",
				"page_kicker": "Inventory",
				"summary_badge_label": "vehicles available",
				"meta_title": "Todde Inventory | Browse certified cars",
				"meta_description": "Explore certified vehicles across sedans, SUVs, and more. Filter by price, year, and transmission to find your next car.",
			},
			{
				"slug": InventoryPageConfig.Slug.REGISTERED,
				"listing_type": CarVariant.ListingType.REGISTERED,
				"title": "Registered Cars",
				"intro_text": "Browse Nigerian-registered vehicles with verified history and trusted ownership records.",
				"page_kicker": "Registered Inventory",
				"summary_badge_label": "registered vehicles",
				"meta_title": "Todde Registered Cars | Locally owned, certified inventory",
				"meta_description": "See registered cars inspected by Todde, ready for quick transfer with transparent documentation.",
			},
			{
				"slug": InventoryPageConfig.Slug.FOREIGN_USED,
				"listing_type": CarVariant.ListingType.FOREIGN_USED,
				"title": "Foreign Used Cars",
				"intro_text": "Shop Tokunbo cars sourced from top international auctions, freshly inspected by Todde.",
				"page_kicker": "Foreign Used",
				"summary_badge_label": "foreign used vehicles",
				"meta_title": "Todde Foreign Used Cars | Tokunbo vehicles you can trust",
				"meta_description": "Discover foreign used vehicles imported by Todde with full inspection reports and financing options.",
			},
		]
		for entry in configs:
			listing_type = entry.pop("listing_type")
			InventoryPageConfig.objects.update_or_create(
				slug=entry.pop("slug"),
				defaults={
					**entry,
					"listing_type": listing_type,
					"is_active": True,
				},
			)

	def _ensure_sample_inventory(self) -> CarVariant:
		manufacturer, _ = CarManufacturer.objects.get_or_create(name="Toyota")
		model, _ = CarModel.objects.get_or_create(
			manufacturer=manufacturer,
			name="Corolla",
			defaults={"body_type": CarModel.BodyType.SEDAN},
		)
		variant, _ = CarVariant.objects.get_or_create(
			model=model,
			year=2023,
			trim="XLE",
			defaults={
				"price": "17800000",
				"transmission": CarVariant.Transmission.AUTOMATIC,
				"listing_type": CarVariant.ListingType.REGISTERED,
			},
		)
		return variant

	def _seed_featured_vehicles(self, variant: CarVariant) -> None:
		entries = [
			{
				"order": 1,
				"variant": variant,
				"name": f"{variant.year} {variant.model.name} {variant.trim}",
				"badge": "Top Choice",
				"location": "Lagos, Nigeria",
				"image_url": "https://images.unsplash.com/photo-1549921296-3b4a6b789555?auto=format&fit=crop&w=800&q=80",
			},
			{
				"order": 2,
				"variant": variant,
				"name": "2022 Honda HR-V Sport",
				"badge": "New Arrival",
				"location": "Abuja, Nigeria",
				"image_url": "https://images.unsplash.com/photo-1563720223185-11003d516935?auto=format&fit=crop&w=800&q=80",
				"price": "₦23,400,000",
				"payment_plan": "₦2,990,000 down • ₦560,000 / month",
			},
		]
		for entry in entries:
			order = entry.pop("order")
			HomepageFeaturedVehicle.objects.update_or_create(
				order=order,
				defaults={
					**entry,
					"is_active": True,
				},
			)

	def _seed_variant_details(self) -> None:
		variants = (
			CarVariant.objects.filter(
				is_active=True,
				model__is_active=True,
				model__manufacturer__is_active=True,
			)
			.select_related("model", "model__manufacturer")
		)
		blueprints = self._variant_blueprints()
		for variant in variants:
			key = self._variant_key(variant)
			blueprint = blueprints.get(key) or self._default_variant_blueprint(variant)
			self._apply_variant_blueprint(variant, blueprint)

	def _variant_key(self, variant: CarVariant) -> tuple[str, str, int, str]:
		trim = variant.trim or ""
		return (
			variant.model.manufacturer.name,
			variant.model.name,
			variant.year,
			trim,
		)

	def _variant_blueprints(self) -> dict[tuple[str, str, int, str], dict[str, object]]:
		return {
			("Toyota", "Corolla", 2024, ""): {
				"detail": {
					"headline": "Efficient daily driver with packed technology",
					"subheadline": "Fresh inspection completed — perfect for Lagos commutes and ride-hailing partners.",
					"description": "The 2024 Toyota Corolla balances reliability, fuel economy, and smart cabin tech. Enjoy Toyota Safety Sense, Android Auto, and an 8-inch infotainment system with crisp audio.",
					"mileage_km": 18250,
					"location": "Lagos, Nigeria",
					"finance_intro": "Spread payments over 24 months with Todde partner banks.",
					"loan_rate": "17.5",
					"loan_deposit_percent": "30",
					"loan_period_months": 24,
					"applicant_types": "Salary earner, Ride-hailing partner, Business owner",
					"is_active": True,
				},
				"images": [
					{"url": "https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?auto=format&fit=crop&w=1600&q=80", "alt": "Toyota Corolla front angle"},
					{"url": "https://images.unsplash.com/photo-1549921296-3b4a6b789555?auto=format&fit=crop&w=1600&q=80", "alt": "Toyota Corolla side profile"},
					{"url": "https://images.unsplash.com/photo-1503736334956-4c8f8e92946d?auto=format&fit=crop&w=1600&q=80", "alt": "Toyota Corolla interior"},
					{"url": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1600&q=80", "alt": "Toyota Corolla rear"},
				],
				"features": [
					"8-inch infotainment display",
					"Toyota Safety Sense 3.0",
					"Apple CarPlay & Android Auto",
					"Dual-zone automatic climate",
				],
				"specs": [
					("Engine", "1.8L inline-4"),
					("Fuel Type", "Petrol"),
					("Transmission", "{transmission}"),
					("Mileage", "18,250 km"),
					("Seating", "5"),
					("Color", "Celestite Grey"),
				],
			},
			("Toyota", "Corolla", 2023, ""): {
				"detail": {
					"headline": "Trusted sedan with complete service history",
					"subheadline": "Certified by Todde engineers and ready for Abuja roads.",
					"description": "Enjoy dependable performance, a comfortable cabin, and stellar resale value. This 2023 Corolla has a comprehensive maintenance record and verified documentation.",
					"mileage_km": 36200,
					"location": "Abuja, Nigeria",
					"finance_intro": "Flexible 24-month repayment window with 30% deposit.",
					"loan_rate": "17.9",
					"loan_deposit_percent": "30",
					"loan_period_months": 24,
					"applicant_types": "Salary earner, Civil servant, Ride-hailing partner",
					"is_active": True,
				},
				"images": [
					{"url": "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?auto=format&fit=crop&w=1600&q=80", "alt": "Toyota Corolla 2023 exterior"},
					{"url": "https://images.unsplash.com/photo-1549924231-f129b911e442?auto=format&fit=crop&w=1600&q=80", "alt": "Toyota Corolla dashboard"},
					{"url": "https://images.unsplash.com/photo-1523983254932-e1e59bff4144?auto=format&fit=crop&w=1600&q=80", "alt": "Toyota Corolla seats"},
				],
				"features": [
					"Reverse camera with guidelines",
					"Fabric premium seats",
					"Digital climate control",
					"Keyless entry",
				],
				"specs": [
					("Engine", "1.8L inline-4"),
					("Fuel Type", "Petrol"),
					("Transmission", "{transmission}"),
					("Mileage", "36,200 km"),
					("Seating", "5"),
					("Color", "Silver"),
				],
			},
			("Toyota", "Corolla", 2023, "XLE"): {
				"detail": {
					"headline": "Redefined compact sedan with bold personality",
					"subheadline": "Inspected and certified by Todde engineers with financing approval in 48 hours.",
					"description": "This Corolla XLE offers dependable performance, premium comfort, and full service history. Perfect for city commutes and ride-hailing operators seeking fuel efficiency and resale value.",
					"mileage_km": 194348,
					"location": "Lagos, Nigeria",
					"finance_intro": "Pay just 30% upfront and spread the balance over flexible tenors.",
					"loan_rate": "17.5",
					"loan_deposit_percent": "30",
					"loan_period_months": 24,
					"applicant_types": "Salary earner, Business owner, Ride-hailing partner",
					"is_active": True,
				},
				"images": [
					{"url": "https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?auto=format&fit=crop&w=1600&q=80", "alt": "Toyota Corolla XLE front"},
					{"url": "https://images.unsplash.com/photo-1549921296-3b4a6b789555?auto=format&fit=crop&w=1600&q=80", "alt": "Toyota Corolla XLE side"},
					{"url": "https://images.unsplash.com/photo-1503736334956-4c8f8e92946d?auto=format&fit=crop&w=1600&q=80", "alt": "Toyota Corolla XLE interior"},
					{"url": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1600&q=80", "alt": "Toyota Corolla XLE rear"},
				],
				"features": [
					"Alloy wheels",
					"Airbag system",
					"Steering control",
					"Navigation system",
					"Reverse camera",
				],
				"specs": [
					("Engine Type", "Cylinder V6"),
					("Fuel Type", "Petrol"),
					("Transmission", "{transmission}"),
					("Mileage", "194,348 km"),
					("Engine Capacity", "4.7L"),
					("Custom Papers", "Available"),
					("Exterior Colour", "Black"),
					("Drive", "All Wheel Drive (AWD)"),
					("Registered", "Yes"),
				],
			},
			("Toyota", "RAV4", 2024, ""): {
				"detail": {
					"headline": "Adventure-ready SUV with advanced safety",
					"subheadline": "Perfect companion for family road trips and business fleets.",
					"description": "The 2024 RAV4 pairs rugged styling with Toyota reliability. Expect dynamic torque vectoring AWD, ample cargo space, and smart driver assists.",
					"mileage_km": 14500,
					"location": "Lagos, Nigeria",
					"finance_intro": "Enjoy 30% down payment with up to 30 months tenor.",
					"loan_rate": "18.0",
					"loan_deposit_percent": "30",
					"loan_period_months": 30,
					"applicant_types": "Business owner, Corporate fleet, Family buyer",
					"is_active": True,
				},
				"images": [
					{"url": "https://images.unsplash.com/photo-1503736334956-4c8f8e92946d?auto=format&fit=crop&w=1600&q=80", "alt": "Toyota RAV4 exterior"},
					{"url": "https://images.unsplash.com/photo-1523983254932-e1e59bff4144?auto=format&fit=crop&w=1600&q=80", "alt": "Toyota RAV4 interior"},
					{"url": "https://images.unsplash.com/photo-1549921296-3b4a6b789555?auto=format&fit=crop&w=1600&q=80", "alt": "Toyota RAV4 rear"},
				],
				"features": [
					"Dynamic torque AWD",
					"Wireless phone charger",
					"Panoramic sunroof",
					"Blind spot monitor",
				],
				"specs": [
					("Engine", "2.5L inline-4"),
					("Fuel Type", "Petrol"),
					("Transmission", "{transmission}"),
					("Mileage", "14,500 km"),
					("Drivetrain", "AWD"),
					("Color", "Magnetic Grey"),
				],
			},
			("Toyota", "RAV4", 2022, ""): {
				"detail": {
					"headline": "Versatile Tokunbo SUV with verified history",
					"subheadline": "All maintenance records confirmed by Todde partners.",
					"description": "This 2022 RAV4 delivers comfort, rugged capability, and efficient performance. Great for corporate fleets and family logistics.",
					"mileage_km": 40200,
					"location": "Port Harcourt, Nigeria",
					"finance_intro": "Bundle insurance, maintenance, and telematics in one plan.",
					"loan_rate": "18.2",
					"loan_deposit_percent": "32",
					"loan_period_months": 30,
					"applicant_types": "Corporate fleet, Ride-hailing partner, Business owner",
					"is_active": True,
				},
				"images": [
					{"url": "https://images.unsplash.com/photo-1504593811423-6dd665756598?auto=format&fit=crop&w=1600&q=80", "alt": "Toyota RAV4 2022 front"},
					{"url": "https://images.unsplash.com/photo-1542282088-fe8426682b8f?auto=format&fit=crop&w=1600&q=80", "alt": "Toyota RAV4 2022 offroad"},
				],
				"features": [
					"Power tailgate",
					"Lane keep assist",
					"Roof rails",
					"Hands-free liftgate",
				],
				"specs": [
					("Engine", "2.5L inline-4"),
					("Fuel Type", "Petrol"),
					("Transmission", "{transmission}"),
					("Mileage", "40,200 km"),
					("Drivetrain", "AWD"),
					("Color", "Blue Flame"),
				],
			},
			("Honda", "Accord", 2023, ""): {
				"detail": {
					"headline": "Executive sedan with turbocharged performance",
					"subheadline": "Ideal for corporate executives and premium ride-hailing services.",
					"description": "Experience 192 hp of turbocharged power, Honda Sensing safety, and ventilated leather seats. The 2023 Accord blends luxury with efficiency.",
					"mileage_km": 21500,
					"location": "Lagos, Nigeria",
					"finance_intro": "Finance up to 36 months with flexible deposits.",
					"loan_rate": "17.8",
					"loan_deposit_percent": "28",
					"loan_period_months": 36,
					"applicant_types": "Corporate executive, Entrepreneur, Ride-hailing elite",
					"is_active": True,
				},
				"images": [
					{"url": "https://images.unsplash.com/photo-1525609004556-c46c7d6cf023?auto=format&fit=crop&w=1600&q=80", "alt": "Honda Accord front"},
					{"url": "https://images.unsplash.com/photo-1549927756-7c66fc0f3c72?auto=format&fit=crop&w=1600&q=80", "alt": "Honda Accord interior"},
				],
				"features": [
					"Ventilated leather seats",
					"Honda Sensing suite",
					"Head-up display",
					"360° parking camera",
				],
				"specs": [
					("Engine", "1.5L turbo inline-4"),
					("Fuel Type", "Petrol"),
					("Transmission", "{transmission}"),
					("Mileage", "21,500 km"),
					("Color", "Platinum White"),
					("Drivetrain", "FWD"),
				],
			},
			("Honda", "Accord", 2021, ""): {
				"detail": {
					"headline": "Certified Tokunbo with impressive comfort",
					"subheadline": "Fully documented import with Todde inspection report.",
					"description": "Enjoy adaptive cruise control, premium audio, and a spacious rear cabin. This Accord is a favourite for premium chauffeurs.",
					"mileage_km": 54800,
					"location": "Abuja, Nigeria",
					"finance_intro": "24-month repayment with maintenance cover included.",
					"loan_rate": "18.1",
					"loan_deposit_percent": "30",
					"loan_period_months": 30,
					"applicant_types": "Ride-hailing premium, Entrepreneur, Salary earner",
					"is_active": True,
				},
				"images": [
					{"url": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=1600&q=80", "alt": "Honda Accord 2021 exterior"},
					{"url": "https://images.unsplash.com/photo-1620892182847-002c0978451d?auto=format&fit=crop&w=1600&q=80", "alt": "Honda Accord 2021 cabin"},
				],
				"features": [
					"Adaptive cruise control",
					"Dual exhaust",
					"Lane departure warning",
					"Wireless smartphone integration",
				],
				"specs": [
					("Engine", "1.5L turbo inline-4"),
					("Fuel Type", "Petrol"),
					("Transmission", "{transmission}"),
					("Mileage", "54,800 km"),
					("Color", "Crystal Black"),
					("Drivetrain", "FWD"),
				],
			},
			("Honda", "CR-V", 2024, ""): {
				"detail": {
					"headline": "Family SUV with panoramic comfort",
					"subheadline": "Ideal for interstate commute and fleet operators requiring efficiency.",
					"description": "This 2024 CR-V offers a roomy interior, walk-away auto lock, and advanced driver assistance. Perfect for large families and corporate mobility.",
					"mileage_km": 16750,
					"location": "Lagos, Nigeria",
					"finance_intro": "Up to 32 months financing with bundled insurance.",
					"loan_rate": "18.4",
					"loan_deposit_percent": "28",
					"loan_period_months": 32,
					"applicant_types": "Logistics partner, Family buyer, Corporate fleet",
					"is_active": True,
				},
				"images": [
					{"url": "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?auto=format&fit=crop&w=1600&q=80", "alt": "Honda CR-V front"},
					{"url": "https://images.unsplash.com/photo-1517677129300-07b130802f46?auto=format&fit=crop&w=1600&q=80", "alt": "Honda CR-V interior"},
				],
				"features": [
					"Hands-free power tailgate",
					"Lane watch camera",
					"Panoramic roof",
					"Heated front seats",
				],
				"specs": [
					("Engine", "1.5L turbo inline-4"),
					("Fuel Type", "Petrol"),
					("Transmission", "{transmission}"),
					("Mileage", "16,750 km"),
					("Drivetrain", "AWD"),
					("Color", "Obsidian Blue"),
				],
			},
			("Honda", "CR-V", 2022, ""): {
				"detail": {
					"headline": "Compact SUV with dependable efficiency",
					"subheadline": "Great for growing families who need space and reliability.",
					"description": "The 2022 CR-V remains a favourite with spacious legroom, Econ driving mode, and a smooth CVT transmission.",
					"mileage_km": 48300,
					"location": "Ibadan, Nigeria",
					"finance_intro": "Spread payments over 28 months with Todde.",
					"loan_rate": "18.6",
					"loan_deposit_percent": "30",
					"loan_period_months": 28,
					"applicant_types": "Family buyer, Logistics partner, Salary earner",
					"is_active": True,
				},
				"images": [
					{"url": "https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?auto=format&fit=crop&w=1600&q=80", "alt": "Honda CR-V 2022 front"},
					{"url": "https://images.unsplash.com/photo-1542293787938-4d2226c9f3e9?auto=format&fit=crop&w=1600&q=80", "alt": "Honda CR-V 2022 rear"},
				],
				"features": [
					"Remote engine start",
					"Power adjustable seats",
					"Dual-zone AC",
					"Smart key entry",
				],
				"specs": [
					("Engine", "1.5L turbo inline-4"),
					("Fuel Type", "Petrol"),
					("Transmission", "{transmission}"),
					("Mileage", "48,300 km"),
					("Drivetrain", "FWD"),
					("Color", "Modern Steel"),
				],
			},
			("Mercedes-Benz", "C300", 2023, ""): {
				"detail": {
					"headline": "Executive luxury with AMG styling",
					"subheadline": "Enjoy MBUX augmented reality and energizing comfort control.",
					"description": "The 2023 C300 delivers 255 hp with a mild hybrid boost. Bask in ambient lighting, Burmester audio, and a 12.3-inch driver display.",
					"mileage_km": 12800,
					"location": "Lagos, Nigeria",
					"finance_intro": "Bundle premium insurance and concierge service with financing.",
					"loan_rate": "16.9",
					"loan_deposit_percent": "35",
					"loan_period_months": 36,
					"applicant_types": "Executive, Entrepreneur, Corporate fleet",
					"is_active": True,
				},
				"images": [
					{"url": "https://images.unsplash.com/photo-1512495967619-2510a1c1c8da?auto=format&fit=crop&w=1600&q=80", "alt": "Mercedes C300 front"},
					{"url": "https://images.unsplash.com/photo-1503736334956-4c8f8e92946d?auto=format&fit=crop&w=1600&q=80", "alt": "Mercedes C300 interior"},
				],
				"features": [
					"AMG line exterior",
					"Burmester 3D audio",
					"Augmented reality navigation",
					"Heated & ventilated seats",
				],
				"specs": [
					("Engine", "2.0L turbo inline-4"),
					("Fuel Type", "Petrol"),
					("Transmission", "{transmission}"),
					("Mileage", "12,800 km"),
					("Drivetrain", "RWD"),
					("Color", "Obsidian Black"),
				],
			},
			("Mercedes-Benz", "C300", 2020, ""): {
				"detail": {
					"headline": "Tokunbo luxury sedan with AMG pack",
					"subheadline": "Meticulously maintained with full customs documentation.",
					"description": "This 2020 C300 comes with adaptive suspension, widescreen cockpit, and a premium leather interior. A great value for luxury seekers.",
					"mileage_km": 61200,
					"location": "Abuja, Nigeria",
					"finance_intro": "Own it outright in 30 months with Todde financing.",
					"loan_rate": "17.2",
					"loan_deposit_percent": "35",
					"loan_period_months": 30,
					"applicant_types": "Executive chauffeur, Entrepreneur, Business owner",
					"is_active": True,
				},
				"images": [
					{"url": "https://images.unsplash.com/photo-1511919884226-fd3cad34687c?auto=format&fit=crop&w=1600&q=80", "alt": "Mercedes C300 2020"},
					{"url": "https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?auto=format&fit=crop&w=1600&q=80", "alt": "Mercedes C300 cabin"},
				],
				"features": [
					"Adaptive suspension",
					"360° camera",
					"Wireless charging",
					"Memory seats",
				],
				"specs": [
					("Engine", "2.0L turbo inline-4"),
					("Fuel Type", "Petrol"),
					("Transmission", "{transmission}"),
					("Mileage", "61,200 km"),
					("Drivetrain", "RWD"),
					("Color", "Iridium Silver"),
				],
			},
			("Mercedes-Benz", "GLA 250", 2024, ""): {
				"detail": {
					"headline": "Compact luxury crossover for urban explorers",
					"subheadline": "MBUX voice assistant, wireless charging, and active brake assist included.",
					"description": "Navigate city streets with elevated seating and a responsive turbo engine. The 2024 GLA 250 delivers sporty dynamics with luxury comfort.",
					"mileage_km": 9800,
					"location": "Lagos, Nigeria",
					"finance_intro": "Structured corporate lease options available via Todde.",
					"loan_rate": "16.5",
					"loan_deposit_percent": "35",
					"loan_period_months": 36,
					"applicant_types": "Corporate fleet, Executive, Luxury chauffeur",
					"is_active": True,
				},
				"images": [
					{"url": "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=1600&q=80", "alt": "Mercedes GLA 250"},
					{"url": "https://images.unsplash.com/photo-1511396279563-50ca07c5e07f?auto=format&fit=crop&w=1600&q=80", "alt": "Mercedes GLA 250 interior"},
				],
				"features": [
					"MBUX infotainment",
					"Wireless charging",
					"LED ambient lighting",
					"Active brake assist",
				],
				"specs": [
					("Engine", "2.0L turbo inline-4"),
					("Fuel Type", "Petrol"),
					("Transmission", "{transmission}"),
					("Mileage", "9,800 km"),
					("Drivetrain", "AWD"),
					("Color", "Polar White"),
				],
			},
			("Mercedes-Benz", "GLA 250", 2021, ""): {
				"detail": {
					"headline": "Compact SUV with German precision",
					"subheadline": "Excellent choice for city logistics and executive shuttles.",
					"description": "The 2021 GLA 250 blends sporty handling with elevated seating. Enjoy dual screens, active parking assist, and premium materials.",
					"mileage_km": 43800,
					"location": "Abuja, Nigeria",
					"finance_intro": "Finance with as low as 35% down over 30 months.",
					"loan_rate": "17.4",
					"loan_deposit_percent": "35",
					"loan_period_months": 30,
					"applicant_types": "Executive chauffeur, Luxury fleet, Entrepreneur",
					"is_active": True,
				},
				"images": [
					{"url": "https://images.unsplash.com/photo-1517414204284-4813654c1b25?auto=format&fit=crop&w=1600&q=80", "alt": "Mercedes GLA 250 2021"},
					{"url": "https://images.unsplash.com/photo-1549922731-8c93c8a78ad4?auto=format&fit=crop&w=1600&q=80", "alt": "Mercedes GLA 250 2021 cabin"},
				],
				"features": [
					"Active parking assist",
					"Power liftgate",
					'Dual 10.25" displays',
					"Keyless-go",
				],
				"specs": [
					("Engine", "2.0L turbo inline-4"),
					("Fuel Type", "Petrol"),
					("Transmission", "{transmission}"),
					("Mileage", "43,800 km"),
					("Drivetrain", "AWD"),
					("Color", "Mountain Grey"),
				],
			},
		}

	def _default_variant_blueprint(self, variant: CarVariant) -> dict[str, object]:
		formatted_mileage = f"{max(variant.year - 2018, 1) * 12000:,} km"
		return {
			"detail": {
				"headline": f"{variant.model.manufacturer.name} {variant.model.name} ready for delivery",
				"subheadline": "Certified by Todde engineers with flexible financing options.",
				"description": f"This {variant.year} {variant.model.name} has passed a 200-point inspection and is available for quick statewide delivery.",
				"mileage_km": (variant.year - 2018) * 12000,
				"location": "Lagos, Nigeria",
				"finance_intro": "Finance with Todde partner banks and get on the road fast.",
				"loan_rate": "18.0",
				"loan_deposit_percent": "30",
				"loan_period_months": 24,
				"applicant_types": "Salary earner, Business owner, Ride-hailing partner",
				"is_active": True,
			},
			"images": [
				{"url": "https://images.unsplash.com/photo-1511919884226-fd3cad34687c?auto=format&fit=crop&w=1600&q=80", "alt": f"{variant.model.manufacturer.name} {variant.model.name} exterior"},
				{"url": "https://images.unsplash.com/photo-1503736334956-4c8f8e92946d?auto=format&fit=crop&w=1600&q=80", "alt": f"{variant.model.manufacturer.name} {variant.model.name} interior"},
			],
			"features": [
				"Air conditioning",
				"Power steering",
				"Anti-lock braking system",
				"Touchscreen infotainment",
			],
			"specs": [
				("Engine", "Efficient powertrain"),
				("Fuel Type", "Petrol"),
				("Transmission", variant.get_transmission_display()),
				("Mileage", formatted_mileage),
				("Body Type", variant.model.get_body_type_display()),
			],
		}

	def _apply_variant_blueprint(self, variant: CarVariant, blueprint: dict[str, object]) -> None:
		detail_defaults = blueprint["detail"].copy()
		CarVariantDetail.objects.update_or_create(
			variant=variant,
			defaults=detail_defaults,
		)

		images = blueprint.get("images", [])
		if images:
			orders_kept: list[int] = []
			for index, image in enumerate(images, start=1):
				orders_kept.append(index)
				CarVariantImage.objects.update_or_create(
					variant=variant,
					order=index,
					defaults={
						"image_url": image["url"],
						"alt_text": image.get("alt", f"{variant.model.manufacturer.name} {variant.model.name}"),
						"is_active": True,
					},
				)
			variant.images.exclude(order__in=orders_kept).delete()

		features = blueprint.get("features", [])
		if features:
			orders_kept = []
			for index, text in enumerate(features, start=1):
				orders_kept.append(index)
				CarVariantFeature.objects.update_or_create(
					variant=variant,
					order=index,
					defaults={
						"text": text,
						"is_active": True,
					},
				)
			variant.features.exclude(order__in=orders_kept).delete()

		specs = blueprint.get("specs", [])
		if specs:
			orders_kept = []
			for index, spec in enumerate(specs, start=1):
				orders_kept.append(index)
				label, value = spec
				if isinstance(value, str):
					value = (
						value.replace("{transmission}", variant.get_transmission_display())
						.replace("{body_type}", variant.model.get_body_type_display())
						.replace("{year}", str(variant.year))
					)
				CarVariantSpecification.objects.update_or_create(
					variant=variant,
					order=index,
					defaults={
						"label": label,
						"value": value,
						"is_active": True,
					},
				)
			variant.specifications.exclude(order__in=orders_kept).delete()
