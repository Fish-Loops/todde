from decimal import Decimal

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .models import (
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


class MarketingPagesTests(TestCase):
	@classmethod
	def setUpTestData(cls):
		manufacturer = CarManufacturer.objects.create(name="Test Manufacturer")
		model = CarModel.objects.create(manufacturer=manufacturer, name="Roadster")
		variant = CarVariant.objects.create(
			model=model,
			year=2024,
			price="25000000",
			transmission=CarVariant.Transmission.AUTOMATIC,
			listing_type=CarVariant.ListingType.FOREIGN_USED,
		)
		CarVariant.objects.create(
			model=model,
			year=2022,
			price="21000000",
			transmission=CarVariant.Transmission.MANUAL,
			listing_type=CarVariant.ListingType.REGISTERED,
		)

		CarVariantDetail.objects.create(
			variant=variant,
			headline="Feature packed coupe",
			subheadline="Premium ride ready for Lagos roads",
			description="Dynamic description for testing detail view integration.",
			mileage_km=123456,
			location="Lagos, Nigeria",
			loan_rate=Decimal("18.0"),
			loan_deposit_percent=Decimal("30"),
			loan_period_months=30,
			applicant_types="Salary earner, Ride-hailing partner",
		)
		CarVariantImage.objects.create(
			variant=variant,
			order=1,
			image_url="https://example.com/image-primary.jpg",
			alt_text="Primary",
		)
		CarVariantFeature.objects.create(variant=variant, order=1, text="Adaptive cruise control")
		CarVariantSpecification.objects.create(variant=variant, order=1, label="Engine", value="V6")

		NavigationLink.objects.create(label="Home", href="/", order=1)
		NavigationLink.objects.create(label="All Cars", href="/cars/", order=2)

		HomepageSectionCopy.objects.bulk_create(
			[
				HomepageSectionCopy(slug="meta", heading="Home | Todde", subheading="Dynamic home"),
				HomepageSectionCopy(slug="categories", heading="Browse by category", subheading="Find what fits"),
				HomepageSectionCopy(slug="featured", heading="Featured", subheading="Editor picks", cta_label="Shop All", cta_url="/cars/"),
				HomepageSectionCopy(slug="value_props", heading="Why Todde", subheading="Reasons you'll love us"),
				HomepageSectionCopy(slug="financing_cta", heading="Unlock financing", subheading="Flexible plans", supporting_text="Decisions within 24 hours", cta_label="See plans", cta_url="/financing/"),
				HomepageSectionCopy(slug="contact", heading="Talk to us", subheading="We're here to help"),
				HomepageSectionCopy(slug="financing_meta", heading="Financing | Todde", subheading="Spread payments smartly"),
			]
		)

		HomepageHero.objects.create(
			title="Own your dream car",
			subtitle="Flexible financing, transparent pricing",
			badge_label="Todde Marketplace",
			primary_cta_label="Start exploring",
			primary_cta_url="/cars/",
			image_url="https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?auto=format&fit=crop&w=1600&q=80",
			order=1,
		)

		HomepageCategory.objects.create(name="Sedans", icon="heroicons:car", description="Comfortable", order=1)
		HomepageCategory.objects.create(name="SUVs", icon="heroicons:truck", description="Spacious", order=2)

		HomepageFeaturedVehicle.objects.create(
			name="Roadster Premium",
			variant=variant,
			badge="Top Choice",
			location="Lagos",
			image_url="https://images.unsplash.com/photo-1549921296-3b4a6b789555?auto=format&fit=crop&w=800&q=80",
			order=1,
		)

		HomepageValueProposition.objects.create(title="Certified quality", description="200-point inspections", icon="heroicons:shield-check", order=1)
		HomepageValueProposition.objects.create(title="Smart pricing", description="Market-aligned", icon="heroicons:banknotes", order=2)

		HomepageFinancingStep.objects.bulk_create(
			[
				HomepageFinancingStep(title=f"Step {idx}", description="Do the thing", order=idx)
				for idx in range(1, 9)
			]
		)

		HomepageFinancingHighlight.objects.create(title="36 months", description="Flexible tenor", order=1)
		HomepageFinancingHighlight.objects.create(title="Low rates", description="Competitive offers", order=2)

		FinancingPageConfig.objects.create(
			slug=FinancingPageConfig.Slug.DEFAULT,
			hero_title="Finance your car in 48 hours",
			hero_subtitle="Dynamic financing content",
			hero_primary_cta_label="Apply now",
			hero_primary_cta_url="/apply/",
			hero_secondary_cta_label="Browse cars",
			hero_secondary_cta_url="/cars/",
			hero_background_image_url="https://example.com/hero.jpg",
			hero_callout_title="Talk to us",
			hero_callout_text="Join our financing clinic every Friday.",
			steps_heading="Steps heading",
			steps_subheading="Steps subheading",
			benefits_heading="Benefits heading",
			benefits_subheading="Benefits subheading",
			eligibility_heading="Eligibility",
			eligibility_description="Eligibility details",
			eligibility_cta_label="See criteria",
			eligibility_cta_url="/criteria/",
			testimonial_image_url="https://example.com/testimonial.jpg",
			testimonial_card_title="Customer spotlight",
			testimonial_card_text="Todde made it happen",
			corporate_heading="Corporate heading",
			corporate_subheading="Corporate subheading",
			corporate_primary_cta_label="Partner CTA",
			corporate_primary_cta_url="mailto:partners@todde.africa",
			corporate_secondary_cta_label="Call CTA",
			corporate_secondary_cta_url="tel:+2347010012345",
			corporate_availability_heading="Available cities",
			corporate_availability_description="Lagos • Abuja",
		)

		FinancingSnapshotItem.objects.bulk_create(
			[
				FinancingSnapshotItem(order=1, text="Snapshot A"),
				FinancingSnapshotItem(order=2, text="Snapshot B"),
			]
		)

		FinancingBenefit.objects.bulk_create(
			[
				FinancingBenefit(order=1, title="Benefit A", description="Description A", icon="heroicons:shield-check"),
				FinancingBenefit(order=2, title="Benefit B", description="Description B", icon="heroicons:banknotes"),
			]
		)

		HomepageBrandMetric.objects.create(value="15K+", label="Customers empowered", order=1)
		HomepageBrandMetric.objects.create(value="48hrs", label="Average approval", order=2)

		HomepageContactCard.objects.create(title="Visit us", description="Plot 24, Admiralty Road, Lekki Phase 1, Lagos.")
		HomepageContactCard.objects.create(
			title="Support",
			description="Talk to us on WhatsApp:",
			link_label="+234 701 001 2345",
			link_url="https://wa.me/2347010012345",
			order=2,
		)

		InventoryPageConfig.objects.bulk_create(
			[
				InventoryPageConfig(
					slug=InventoryPageConfig.Slug.ALL,
					listing_type="",
					title="All Cars",
					intro_text="Discover the entire marketplace",
					page_kicker="Inventory",
					summary_badge_label="vehicles available",
					meta_title="All Cars | Todde",
					meta_description="Browse every certified vehicle available on Todde.",
				),
				InventoryPageConfig(
					slug=InventoryPageConfig.Slug.REGISTERED,
					listing_type=CarVariant.ListingType.REGISTERED,
					title="Registered Cars",
					intro_text="In-country, ready to transfer",
					page_kicker="Registered Inventory",
					summary_badge_label="registered vehicles",
					meta_title="Registered Cars | Todde",
					meta_description="See locally registered, Todde-certified inventory.",
				),
				InventoryPageConfig(
					slug=InventoryPageConfig.Slug.FOREIGN_USED,
					listing_type=CarVariant.ListingType.FOREIGN_USED,
					title="Foreign Used Cars",
					intro_text="Tokunbo inventory",
					page_kicker="Foreign Used",
					summary_badge_label="foreign used vehicles",
					meta_title="Foreign Used Cars | Todde",
					meta_description="Import-ready cars vetted by Todde.",
				),
			]
		)

	def test_homepage_renders(self):
		response = self.client.get(reverse("marketing:home"))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "marketing/home.html")
		self.assertIn("nav_links", response.context)
		self.assertGreater(response.context["nav_links"].count(), 0)
		self.assertIsNotNone(response.context.get("hero"))
		self.assertEqual(response.context["categories"].count(), 2)
		self.assertGreater(response.context["featured_vehicles"].count(), 0)
		self.assertIn("section_copy", response.context)
		self.assertGreater(response.context["car_manufacturers"].count(), 0)

	def test_financing_page_renders(self):
		response = self.client.get(reverse("marketing:financing"))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "marketing/financing.html")
		self.assertIn("financing_steps", response.context)
		self.assertEqual(response.context["financing_steps"].count(), 8)
		self.assertEqual(response.context["hero_title"], "Finance your car in 48 hours")
		self.assertEqual(len(response.context["financing_snapshot_items"]), 2)
		self.assertEqual(len(response.context["financing_benefits"]), 2)
		self.assertEqual(response.context["eligibility"]["cta_label"], "See criteria")
		self.assertEqual(response.context["corporate"]["heading"], "Corporate heading")

	def test_car_models_api_requires_manufacturer(self):
		response = self.client.get(reverse("marketing:api_car_models"))
		self.assertEqual(response.status_code, 400)
		self.assertJSONEqual(response.content, {"error": "Missing manufacturer parameter."})

	def test_car_models_api_returns_models(self):
		manufacturer = CarManufacturer.objects.first()
		response = self.client.get(reverse("marketing:api_car_models"), {"manufacturer": manufacturer.id})
		self.assertEqual(response.status_code, 200)
		payload = response.json()
		self.assertEqual(payload["manufacturer"]["id"], manufacturer.id)
		self.assertEqual(len(payload["models"]), manufacturer.models.count())

	def test_car_variants_api_returns_variants(self):
		model = CarModel.objects.first()
		response = self.client.get(reverse("marketing:api_car_variants"), {"model": model.id})
		self.assertEqual(response.status_code, 200)
		payload = response.json()
		self.assertEqual(payload["model"]["id"], model.id)
		self.assertEqual(len(payload["variants"]), model.variants.count())

	def test_all_cars_page_renders(self):
		response = self.client.get(reverse("marketing:all_cars"))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "marketing/inventory.html")
		self.assertIn("page_obj", response.context)
		self.assertGreater(response.context["total_results"], 0)
		self.assertEqual(response.context["page_title"], "All Cars")
		self.assertEqual(response.context["summary_badge_label"], "vehicles available")
		self.assertIsNotNone(response.context["page_config"])
		first_variant = response.context["page_obj"].object_list[0]
		self.assertIn("/cars/", reverse("marketing:vehicle_detail", args=[first_variant.id]))

	def test_vehicle_detail_page_renders(self):
		variant = CarVariantDetail.objects.select_related("variant").first().variant
		response = self.client.get(reverse("marketing:vehicle_detail", args=[variant.id]))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "marketing/vehicle_detail.html")
		self.assertIn("features", response.context)
		self.assertGreaterEqual(len(response.context["features"]), 1)
		self.assertIn("specifications", response.context)
		self.assertIn("loan_summary", response.context)
		self.assertEqual(response.context["loan_summary"]["period_months"], 30)
		self.assertIn("gallery", response.context)
		self.assertTrue(response.context["gallery"])
		self.assertIn("applicant_types", response.context)
		self.assertGreaterEqual(len(response.context["applicant_types"]), 1)

	def test_all_cars_filters_by_transmission(self):
		url = reverse("marketing:all_cars")
		response = self.client.get(url, {"transmission": CarVariant.Transmission.MANUAL})
		self.assertEqual(response.status_code, 200)
		page_obj = response.context["page_obj"]
		self.assertTrue(all(item.transmission == CarVariant.Transmission.MANUAL for item in page_obj.object_list))

	def test_registered_cars_page_filters_listing_type(self):
		response = self.client.get(reverse("marketing:registered_cars"))
		self.assertEqual(response.status_code, 200)
		page_obj = response.context["page_obj"]
		self.assertTrue(all(item.listing_type == CarVariant.ListingType.REGISTERED for item in page_obj.object_list))
		self.assertEqual(response.context["page_title"], "Registered Cars")
		self.assertEqual(response.context["summary_badge_label"], "registered vehicles")
		self.assertEqual(response.context["page_config"].slug, InventoryPageConfig.Slug.REGISTERED)

	def test_foreign_used_page_filters_listing_type(self):
		response = self.client.get(reverse("marketing:foreign_used_cars"))
		self.assertEqual(response.status_code, 200)
		page_obj = response.context["page_obj"]
		self.assertTrue(all(item.listing_type == CarVariant.ListingType.FOREIGN_USED for item in page_obj.object_list))
		self.assertEqual(response.context["summary_badge_label"], "foreign used vehicles")
		self.assertEqual(response.context["page_config"].slug, InventoryPageConfig.Slug.FOREIGN_USED)

	def test_seed_homepage_command_is_idempotent(self):
		nav_count_before = NavigationLink.objects.count()
		category_count_before = HomepageCategory.objects.count()
		config_count_before = InventoryPageConfig.objects.count()
		financing_config_before = FinancingPageConfig.objects.count()
		snapshot_count_before = FinancingSnapshotItem.objects.count()
		benefit_count_before = FinancingBenefit.objects.count()
		variant_detail_before = CarVariantDetail.objects.count()
		variant_image_before = CarVariantImage.objects.count()
		variant_feature_before = CarVariantFeature.objects.count()
		variant_spec_before = CarVariantSpecification.objects.count()
		call_command("seed_homepage")
		self.assertGreaterEqual(NavigationLink.objects.count(), nav_count_before)
		self.assertGreaterEqual(HomepageCategory.objects.count(), category_count_before)
		self.assertGreaterEqual(InventoryPageConfig.objects.count(), config_count_before)
		self.assertGreaterEqual(InventoryPageConfig.objects.filter(is_active=True).count(), 3)
		self.assertGreaterEqual(FinancingPageConfig.objects.count(), financing_config_before)
		self.assertGreaterEqual(FinancingSnapshotItem.objects.count(), snapshot_count_before)
		self.assertGreaterEqual(FinancingBenefit.objects.count(), benefit_count_before)
		self.assertGreaterEqual(CarVariantDetail.objects.count(), variant_detail_before)
		self.assertGreaterEqual(CarVariantImage.objects.count(), variant_image_before)
		self.assertGreaterEqual(CarVariantFeature.objects.count(), variant_feature_before)
		self.assertGreaterEqual(CarVariantSpecification.objects.count(), variant_spec_before)
		for seeded_variant in CarVariant.objects.all():
			detail = CarVariantDetail.objects.filter(variant=seeded_variant, is_active=True).first()
			self.assertIsNotNone(detail, f"Variant {seeded_variant} missing detail after seeding")
			self.assertGreater(CarVariantImage.objects.filter(variant=seeded_variant, is_active=True).count(), 0)
			self.assertGreater(CarVariantFeature.objects.filter(variant=seeded_variant, is_active=True).count(), 0)
			self.assertGreater(CarVariantSpecification.objects.filter(variant=seeded_variant, is_active=True).count(), 0)
			self.assertTrue(detail.applicant_type_choices, f"Variant {seeded_variant} detail missing applicant types")
		call_command("seed_homepage")
		self.assertEqual(NavigationLink.objects.count(), NavigationLink.objects.values("label").distinct().count())
		self.assertEqual(HomepageCategory.objects.count(), HomepageCategory.objects.values("name").distinct().count())
		self.assertEqual(InventoryPageConfig.objects.count(), InventoryPageConfig.objects.values("slug").distinct().count())
		self.assertEqual(FinancingPageConfig.objects.count(), FinancingPageConfig.objects.values("slug").distinct().count())
		self.assertEqual(FinancingSnapshotItem.objects.count(), FinancingSnapshotItem.objects.values("text").distinct().count())
		self.assertEqual(FinancingBenefit.objects.count(), FinancingBenefit.objects.values("title").distinct().count())
		self.assertEqual(CarVariantDetail.objects.count(), CarVariantDetail.objects.values("variant").distinct().count())
		self.assertEqual(CarVariantImage.objects.count(), CarVariantImage.objects.values("variant", "image_url").distinct().count())
		self.assertEqual(CarVariantFeature.objects.count(), CarVariantFeature.objects.values("variant", "text").distinct().count())
		self.assertEqual(CarVariantSpecification.objects.count(), CarVariantSpecification.objects.values("variant", "label").distinct().count())
