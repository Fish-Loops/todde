from decimal import Decimal, InvalidOperation, ROUND_HALF_UP, getcontext
from types import SimpleNamespace
from urllib.parse import urlencode
from collections import defaultdict

from django.core.paginator import Paginator
from django.db.models import Count, Max, Min, Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.templatetags.static import static
from django.views.decorators.http import require_GET

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


def _build_section_copy_map():
	default_factory = lambda: SimpleNamespace(heading="", subheading="", supporting_text="", cta_label="", cta_url="")
	mapping = defaultdict(default_factory)
	for entry in HomepageSectionCopy.objects.filter(is_active=True):
		mapping[entry.slug] = entry
	return mapping


def homepage(request):
	section_copy = _build_section_copy_map()
	hero_slides = HomepageHero.objects.filter(is_active=True).order_by("order")
	categories = HomepageCategory.objects.filter(is_active=True).order_by("order")
	featured = (
		HomepageFeaturedVehicle.objects.filter(is_active=True)
		.select_related("variant", "variant__model", "variant__model__manufacturer")
		.prefetch_related(
			Prefetch(
				"variant__images",
				queryset=CarVariantImage.objects.filter(is_active=True).order_by("order", "id"),
			)
		)
	)
	value_props = HomepageValueProposition.objects.filter(is_active=True)
	brand_metrics = HomepageBrandMetric.objects.filter(is_active=True)
	financing_highlights = HomepageFinancingHighlight.objects.filter(is_active=True)
	nav_links = NavigationLink.objects.filter(is_active=True)
	financing_steps = HomepageFinancingStep.objects.filter(is_active=True)
	contact_cards = HomepageContactCard.objects.filter(is_active=True)

	placeholder_image_url = static("images/vehicle-placeholder.svg")
	featured_list = []
	for vehicle in featured:
		display_url = placeholder_image_url
		display_alt = vehicle.name
		is_placeholder = True
		if vehicle.variant:
			image_info = _resolve_variant_primary_image(vehicle.variant, placeholder_image_url)
			display_url = image_info.source_url
			display_alt = image_info.alt_text or vehicle.name
			is_placeholder = image_info.is_placeholder
		elif vehicle.image_url:
			display_url = vehicle.image_url
			display_alt = vehicle.name
			is_placeholder = False
		vehicle.display_image_url = display_url
		vehicle.display_image_alt = display_alt
		vehicle.display_image_is_placeholder = is_placeholder
		featured_list.append(vehicle)

	context = {
		"nav_links": nav_links,
		"hero_slides": hero_slides,
		"categories": categories,
		"featured_vehicles": featured_list,
		"value_props": value_props,
		"brand_metrics": brand_metrics,
		"financing_highlights": financing_highlights,
		"financing_steps": financing_steps,
		"contact_cards": contact_cards,
		"section_copy": section_copy,
		"car_manufacturers": CarManufacturer.objects.filter(is_active=True).order_by("name"),
		"meta": {
			"title": section_copy["meta"].heading or "Todde Integrated Services | Empowering Nigerians to own cars with flexible financing",
			"description": section_copy["meta"].subheading or "Shop certified vehicles, access Todde's flexible financing, and drive home with confidence in 48 hours.",
		},
	}
	return render(request, "marketing/home.html", context)


def financing(request):
	section_copy = _build_section_copy_map()
	config = FinancingPageConfig.objects.filter(is_active=True).order_by("slug").first()

	defaults = {
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
	}

	def resolve(field: str) -> str:
		if config:
			return config.resolve(field, defaults[field])
		return defaults[field]

	snapshot_items = list(
		FinancingSnapshotItem.objects.filter(is_active=True).order_by("order", "id")
	)
	if not snapshot_items:
		snapshot_items = [
			SimpleNamespace(text="Pay only 30% upfront and get your keys within 48 hours of approval."),
			SimpleNamespace(text="Automated payment reminders and flexible repayment channels."),
			SimpleNamespace(text="Roadside assistance, insurance, and maintenance bundles included."),
		]

	benefits = list(
		FinancingBenefit.objects.filter(is_active=True).order_by("order", "id")
	)
	if not benefits:
		benefits = [
			SimpleNamespace(title="Comprehensive insurance", description="Comprehensive insurance coverage and annual renewals handled by Todde.", icon="heroicons:shield-check"),
			SimpleNamespace(title="Dedicated support", description="Dedicated support agents for servicing, documentation, and payment plans.", icon="heroicons:lifebuoy"),
			SimpleNamespace(title="Transparent pricing", description="Transparent pricing and zero hidden charges on every contract.", icon="heroicons:banknotes"),
		]
	context = {
		"nav_links": NavigationLink.objects.filter(is_active=True),
		"financing_steps": HomepageFinancingStep.objects.filter(is_active=True),
		"financing_highlights": HomepageFinancingHighlight.objects.filter(is_active=True),
		"financing_snapshot_items": snapshot_items,
		"financing_benefits": benefits,
		"hero_background_image_url": resolve("hero_background_image_url"),
		"hero_primary_cta": {
			"label": resolve("hero_primary_cta_label"),
			"url": resolve("hero_primary_cta_url"),
		},
		"hero_secondary_cta": {
			"label": resolve("hero_secondary_cta_label"),
			"url": resolve("hero_secondary_cta_url"),
		},
		"hero_title": resolve("hero_title"),
		"hero_subtitle": resolve("hero_subtitle"),
		"hero_callout_title": resolve("hero_callout_title"),
		"hero_callout_text": resolve("hero_callout_text"),
		"steps_heading": resolve("steps_heading"),
		"steps_subheading": resolve("steps_subheading"),
		"benefits_heading": resolve("benefits_heading"),
		"benefits_subheading": resolve("benefits_subheading"),
		"eligibility": {
			"heading": resolve("eligibility_heading"),
			"description": resolve("eligibility_description"),
			"cta_label": resolve("eligibility_cta_label"),
			"cta_url": resolve("eligibility_cta_url"),
		},
		"testimonial": {
			"image_url": resolve("testimonial_image_url"),
			"card_title": resolve("testimonial_card_title"),
			"card_text": resolve("testimonial_card_text"),
		},
		"corporate": {
			"heading": resolve("corporate_heading"),
			"subheading": resolve("corporate_subheading"),
			"primary_label": resolve("corporate_primary_cta_label"),
			"primary_url": resolve("corporate_primary_cta_url"),
			"secondary_label": resolve("corporate_secondary_cta_label"),
			"secondary_url": resolve("corporate_secondary_cta_url"),
			"availability_heading": resolve("corporate_availability_heading"),
			"availability_description": resolve("corporate_availability_description"),
		},
		"page_config": config,
		"meta": {
			"title": section_copy["financing_meta"].heading or "Todde Car Financing | Spread payments and own your dream car",
			"description": section_copy["financing_meta"].subheading or "Pay only 30% upfront and finance the rest with Todde. See how our 8-step process gets you on the road fast.",
		},
	}
	return render(request, "marketing/financing.html", context)


def _parse_decimal(value: str | None) -> Decimal | None:
	if not value:
		return None
	try:
		return Decimal(value)
	except (InvalidOperation, TypeError):
		return None


def _parse_int(value: str | None) -> int | None:
	if not value:
		return None
	try:
		return int(value)
	except (TypeError, ValueError):
		return None


def _encode_filters(selected_filters: dict[str, object]) -> str:
	params: list[tuple[str, str]] = []
	for key, value in selected_filters.items():
		if key == "transmission":
			for transmission_value in value:
				params.append(("transmission", str(transmission_value)))
		else:
			params.append((key, str(value)))
	return urlencode(params)


def _compute_financing_summary(
	*,
	price: Decimal,
	rate_percent: Decimal,
	deposit_percent: Decimal,
	period_months: int,
) -> dict[str, object]:
	getcontext().prec = 28
	if price is None or price <= 0 or period_months <= 0:
		return {
			"loan_amount": Decimal("0"),
			"deposit_amount": Decimal("0"),
			"monthly_payment": Decimal("0"),
		}
	deposit_amount = (price * deposit_percent / Decimal("100")).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
	loan_amount = (price - deposit_amount).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
	rate_per_month = (rate_percent / Decimal("100")) / Decimal("12")
	if rate_per_month <= 0:
		monthly_payment = (loan_amount / period_months).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
	else:
		factor = (Decimal("1") + rate_per_month) ** period_months
		monthly_payment = (loan_amount * rate_per_month * factor / (factor - Decimal("1"))).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
	return {
		"deposit_amount": deposit_amount,
		"loan_amount": loan_amount,
		"monthly_payment": monthly_payment,
		"period_months": period_months,
		"rate_percent": rate_percent,
		"deposit_percent": deposit_percent,
	}


def _resolve_variant_primary_image(variant: CarVariant, placeholder_url: str) -> SimpleNamespace:
	manufacturer_name = variant.model.manufacturer.name if variant.model and variant.model.manufacturer else ""
	model_name = variant.model.name if variant.model else ""
	year_value = getattr(variant, "year", "")
	default_alt_components = [component for component in (manufacturer_name, model_name, year_value) if component]
	default_alt_text = " ".join(map(str, default_alt_components)) or "Todde vehicle"
	images_manager = getattr(variant, "images", None)
	if images_manager is not None:
		image_candidates = images_manager.all()
		for image in image_candidates:
			source = getattr(image, "source_url", "") or ""
			source = source.strip()
			if source:
				alt_text = getattr(image, "alt_text", "") or default_alt_text
				return SimpleNamespace(
					source_url=source,
					alt_text=alt_text,
					is_placeholder=False,
				)
	return SimpleNamespace(
		source_url=placeholder_url,
		alt_text=default_alt_text,
		is_placeholder=True,
	)


def _inventory_queryset(listing_type: str | None = None):
	queryset = (
		CarVariant.objects.filter(
			is_active=True,
			model__is_active=True,
			model__manufacturer__is_active=True,
		)
		.select_related("model", "model__manufacturer")
		.prefetch_related(
			Prefetch(
				"images",
				queryset=CarVariantImage.objects.filter(is_active=True).order_by("order", "id"),
			)
		)
	)
	if listing_type:
		queryset = queryset.filter(listing_type=listing_type)
	return queryset


def _resolve_inventory_copy(
	slug: str,
	*,
	default_title: str,
	default_intro: str,
	default_meta_title: str,
	default_meta_description: str,
	default_kicker: str,
	default_summary_label: str,
):
	config = InventoryPageConfig.objects.filter(slug=slug, is_active=True).first()
	if not config:
		return {
			"config": None,
			"page_title": default_title,
			"intro_text": default_intro,
			"page_kicker": default_kicker,
			"summary_badge_label": default_summary_label,
			"meta_title": default_meta_title,
			"meta_description": default_meta_description,
		}

	return {
		"config": config,
		"page_title": config.resolved_page_title(default_title),
		"intro_text": config.resolved_intro(default_intro),
		"page_kicker": config.resolved_kicker(default_kicker),
		"summary_badge_label": config.resolved_summary_label(default_summary_label),
		"meta_title": config.resolved_meta_title(default_meta_title),
		"meta_description": config.resolved_meta_description(default_meta_description),
	}


def _generate_dynamic_title(selected_filters: dict[str, object], default_title: str) -> str:
	"""Generate a dynamic title based on applied filters."""
	manufacturer_id = selected_filters.get("manufacturer")
	model_id = selected_filters.get("model")
	year = selected_filters.get("year")
	
	title_parts = []
	
	# Get manufacturer name if filtered by manufacturer
	if manufacturer_id:
		try:
			manufacturer = CarManufacturer.objects.get(id=manufacturer_id, is_active=True)
			title_parts.append(manufacturer.name)
		except CarManufacturer.DoesNotExist:
			pass
	
	# Get model name if filtered by model
	if model_id:
		try:
			model = CarModel.objects.get(id=model_id, is_active=True)
			if not manufacturer_id:  # If manufacturer wasn't already added
				title_parts.append(model.manufacturer.name)
			title_parts.append(model.name)
		except CarModel.DoesNotExist:
			pass
	
	# Add year if specified
	if year:
		title_parts.append(str(year))
	
	# Build the title
	if title_parts:
		if len(title_parts) == 1:
			return f"{title_parts[0]} Cars"
		elif len(title_parts) == 2:
			return f"{title_parts[0]} {title_parts[1]} Cars"
		else:
			return f"{' '.join(title_parts)} Cars"
	
	return default_title


def _build_inventory_context(
	request,
	*,
	listing_type: str | None,
	page_slug: str,
	default_page_title: str,
	default_intro_text: str,
	default_meta_title: str,
	default_meta_description: str,
	default_page_kicker: str = "Inventory",
	default_summary_badge_label: str = "vehicles available",
):
	base_queryset = _inventory_queryset(listing_type=listing_type)

	available_stats = base_queryset.aggregate(
		min_price=Min("price"),
		max_price=Max("price"),
		min_year=Min("year"),
		max_year=Max("year"),
	)

	category_counts = {
		entry["model__body_type"]: entry["total"]
		for entry in base_queryset.values("model__body_type").annotate(total=Count("id"))
	}
	available_categories = [
		{
			"value": body_value,
			"label": body_label,
			"count": category_counts.get(body_value, 0),
		}
		for body_value, body_label in CarModel.BodyType.choices
		if category_counts.get(body_value, 0) > 0
	]

	transmission_counts = {
		entry["transmission"]: entry["total"]
		for entry in base_queryset.values("transmission").annotate(total=Count("id"))
	}
	available_transmissions = [
		{
			"value": transmission_value,
			"label": CarVariant.Transmission(transmission_value).label,
			"count": transmission_counts.get(transmission_value, 0),
		}
		for transmission_value, _ in CarVariant.Transmission.choices
		if transmission_counts.get(transmission_value, 0) > 0
	]

	selected_filters: dict[str, object] = {}
	filtered_queryset = base_queryset

	price_min = _parse_decimal(request.GET.get("price_min"))
	price_max = _parse_decimal(request.GET.get("price_max"))
	if price_min is not None:
		filtered_queryset = filtered_queryset.filter(price__gte=price_min)
		selected_filters["price_min"] = price_min
	if price_max is not None:
		filtered_queryset = filtered_queryset.filter(price__lte=price_max)
		selected_filters["price_max"] = price_max

	year_min = _parse_int(request.GET.get("year_min"))
	year_max = _parse_int(request.GET.get("year_max"))
	if year_min is not None:
		filtered_queryset = filtered_queryset.filter(year__gte=year_min)
		selected_filters["year_min"] = year_min
	if year_max is not None:
		filtered_queryset = filtered_queryset.filter(year__lte=year_max)
		selected_filters["year_max"] = year_max

	category_value = request.GET.get("category")
	if category_value in dict(CarModel.BodyType.choices):
		filtered_queryset = filtered_queryset.filter(model__body_type=category_value)
		selected_filters["category"] = category_value

	transmission_values = [value for value in request.GET.getlist("transmission") if value in dict(CarVariant.Transmission.choices)]
	if transmission_values:
		filtered_queryset = filtered_queryset.filter(transmission__in=transmission_values)
		selected_filters["transmission"] = transmission_values

	# Manufacturer filtering
	manufacturer_id = _parse_int(request.GET.get("manufacturer"))
	if manufacturer_id is not None:
		filtered_queryset = filtered_queryset.filter(model__manufacturer__id=manufacturer_id)
		selected_filters["manufacturer"] = manufacturer_id

	# Model filtering
	model_id = _parse_int(request.GET.get("model"))
	if model_id is not None:
		filtered_queryset = filtered_queryset.filter(model__id=model_id)
		selected_filters["model"] = model_id

	# Exact year filtering (different from year range)
	year = _parse_int(request.GET.get("year"))
	if year is not None:
		filtered_queryset = filtered_queryset.filter(year=year)
		selected_filters["year"] = year

	sort_key = request.GET.get("sort", "price_low_high")
	sort_mappings = {
		"price_low_high": "price",
		"price_high_low": "-price",
		"year_new_old": "-year",
		"year_old_new": "year",
	}
	ordering = sort_mappings.get(sort_key, "price")
	selected_filters["sort"] = sort_key if sort_key in sort_mappings else "price_low_high"

	filtered_queryset = filtered_queryset.order_by(ordering, "model__manufacturer__name")

	paginator = Paginator(filtered_queryset, 12)
	page_number = request.GET.get("page")
	page_obj = paginator.get_page(page_number)

	encoded_filters = _encode_filters({k: v for k, v in selected_filters.items() if k != "sort"})

	placeholder_image_url = static("images/vehicle-placeholder.svg")
	for variant in page_obj:
		image_info = _resolve_variant_primary_image(variant, placeholder_image_url)
		variant.display_image = image_info.source_url
		variant.display_image_url = image_info.source_url
		variant.display_image_alt = image_info.alt_text or f"{variant.model.manufacturer.name} {variant.model.name}"
		variant.display_image_is_placeholder = image_info.is_placeholder

	# Generate dynamic title based on filters
	dynamic_title = _generate_dynamic_title(selected_filters, default_page_title)

	copy = _resolve_inventory_copy(
		page_slug,
		default_title=dynamic_title,
		default_intro=default_intro_text,
		default_meta_title=default_meta_title,
		default_meta_description=default_meta_description,
		default_kicker=default_page_kicker,
		default_summary_label=default_summary_badge_label,
	)

	context = {
		"nav_links": NavigationLink.objects.filter(is_active=True),
		"meta": {
			"title": copy["meta_title"],
			"description": copy["meta_description"],
		},
		"page_obj": page_obj,
		"total_results": paginator.count,
		"available_stats": available_stats,
		"available_categories": available_categories,
		"available_transmissions": available_transmissions,
		"selected_filters": selected_filters,
		"selected_category": selected_filters.get("category"),
		"selected_transmissions": selected_filters.get("transmission", []),
		"selected_sort": selected_filters.get("sort", "price_low_high"),
		"filters_querystring": encoded_filters,
		"sort_options": [
			{"value": "price_low_high", "label": "Price: Low to High"},
			{"value": "price_high_low", "label": "Price: High to Low"},
			{"value": "year_new_old", "label": "Year: New to Old"},
			{"value": "year_old_new", "label": "Year: Old to New"},
		],
		"page_kicker": copy["page_kicker"],
		"page_title": copy["page_title"],
		"intro_text": copy["intro_text"],
		"summary_badge_label": copy["summary_badge_label"],
		"page_config": copy["config"],
	}
	return context


def all_cars(request):
	context = _build_inventory_context(
		request,
		listing_type=None,
		page_slug=InventoryPageConfig.Slug.ALL,
		default_page_title="All Cars",
		default_intro_text="Discover certified cars inspected by Todde. Use the filters to zero in on the right price, year, transmission, or body style.",
		default_meta_title="Todde Inventory | Browse certified cars",
		default_meta_description="Explore certified vehicles across sedans, SUVs, and more. Filter by price, year, and transmission to find your next car.",
	)
	return render(request, "marketing/inventory.html", context)


def registered_cars(request):
	context = _build_inventory_context(
		request,
		listing_type=CarVariant.ListingType.REGISTERED,
		page_slug=InventoryPageConfig.Slug.REGISTERED,
		default_page_title="Registered Cars",
		default_intro_text="Browse Nigerian-registered vehicles with verified history and trusted ownership records.",
		default_meta_title="Todde Registered Cars | Locally owned, certified inventory",
		default_meta_description="See registered cars inspected by Todde, ready for quick transfer with transparent documentation.",
		default_summary_badge_label="registered vehicles",
	)
	return render(request, "marketing/inventory.html", context)


def foreign_used_cars(request):
	context = _build_inventory_context(
		request,
		listing_type=CarVariant.ListingType.FOREIGN_USED,
		page_slug=InventoryPageConfig.Slug.FOREIGN_USED,
		default_page_title="Foreign Used Cars",
		default_intro_text="Shop Tokunbo cars sourced from top international auctions, freshly inspected by Todde.",
		default_meta_title="Todde Foreign Used Cars | Tokunbo vehicles you can trust",
		default_meta_description="Discover foreign used vehicles imported by Todde with full inspection reports and financing options.",
		default_summary_badge_label="foreign used vehicles",
	)
	return render(request, "marketing/inventory.html", context)


def vehicle_detail(request, variant_id: int):
	variant_queryset = (
		CarVariant.objects.filter(
			pk=variant_id,
			is_active=True,
			model__is_active=True,
			model__manufacturer__is_active=True,
		)
		.select_related("model", "model__manufacturer", "detail")
		.prefetch_related(
			Prefetch("images", queryset=CarVariantImage.objects.filter(is_active=True).order_by("order", "id")),
			Prefetch("features", queryset=CarVariantFeature.objects.filter(is_active=True).order_by("order", "id")),
			Prefetch("specifications", queryset=CarVariantSpecification.objects.filter(is_active=True).order_by("order", "id")),
		)
	)
	variant = get_object_or_404(variant_queryset)
	detail: CarVariantDetail | None = getattr(variant, "detail", None)
	if detail and not detail.is_active:
		detail = None

	placeholder_image_url = static("images/vehicle-placeholder.svg")
	gallery: list[SimpleNamespace] = []
	placeholder_items: list[SimpleNamespace] = []
	for image in variant.images.all():
		raw_source = (image.source_url or "").strip()
		resolved_source = raw_source or placeholder_image_url
		entry = SimpleNamespace(
			source_url=resolved_source,
			alt_text=image.alt_text or f"{variant.model.manufacturer.name} {variant.model.name}",
			is_placeholder=resolved_source == placeholder_image_url,
		)
		if entry.is_placeholder:
			placeholder_items.append(entry)
		else:
			gallery.append(entry)

	if not gallery:
		gallery = [
			SimpleNamespace(
				source_url=placeholder_image_url,
				alt_text=f"{variant.model.manufacturer.name} {variant.model.name}",
				is_placeholder=True,
			)
		]
	else:
		gallery.extend(placeholder_items)

	primary_gallery_image = gallery[0] if gallery else None
	gallery_thumbnails = [item for item in gallery[1:] if not item.is_placeholder]
	features = list(variant.features.all()) or [
		SimpleNamespace(text="Alloy wheels"),
		SimpleNamespace(text="Airbags"),
		SimpleNamespace(text="Steering control"),
		SimpleNamespace(text="Navigation system"),
	]
	specifications = list(variant.specifications.all())
	if not specifications:
		specifications = [
			SimpleNamespace(label="Engine Type", value="Cylinder V6"),
			SimpleNamespace(label="Fuel Type", value="Petrol"),
			SimpleNamespace(label="Transmission", value=variant.get_transmission_display()),
			SimpleNamespace(label="Mileage", value=detail.mileage_display if detail else "—"),
		]

	rate_percent = Decimal(detail.loan_rate) if detail and detail.loan_rate is not None else Decimal("17.5")
	deposit_percent = Decimal(detail.loan_deposit_percent) if detail and detail.loan_deposit_percent is not None else Decimal("30")
	period_months = int(detail.loan_period_months) if detail and detail.loan_period_months is not None else 24
	loan_summary = _compute_financing_summary(
		price=variant.price,
		rate_percent=rate_percent,
		deposit_percent=deposit_percent,
		period_months=period_months,
	)
	applicant_types = detail.applicant_type_choices if detail and detail.applicant_type_choices else [
		"Salary Earner",
		"Business Owner",
		"Ride-Hailing Partner",
	]

	related_variants = (
		CarVariant.objects.filter(
			is_active=True,
			model__manufacturer=variant.model.manufacturer,
		)
		.exclude(pk=variant.pk)
		.select_related("model", "model__manufacturer")
		.order_by("-year")[:3]
	)

	categories = [
		{
			"label": label,
			"value": value,
			"url": f"/cars/?category={value}",
		}
		for value, label in CarModel.BodyType.choices
	]
	manufacturers = CarManufacturer.objects.filter(is_active=True).order_by("name")[:10]
	recent_variants = (
		CarVariant.objects.filter(is_active=True)
		.select_related("model", "model__manufacturer")
		.order_by("-updated_at")[:3]
	)

	context = {
		"nav_links": NavigationLink.objects.filter(is_active=True),
		"variant": variant,
		"detail": detail,
		"gallery": gallery,
		"primary_gallery_image": primary_gallery_image,
		"gallery_thumbnails": gallery_thumbnails,
		"features": features,
		"specifications": specifications,
		"loan_summary": loan_summary,
		"applicant_types": applicant_types,
		"related_variants": related_variants,
		"categories": categories,
		"manufacturers": manufacturers,
		"recent_variants": recent_variants,
		"meta": {
			"title": f"{variant.model.manufacturer.name} {variant.model.name} {variant.year} | Todde",
			"description": (detail.description[:155] if detail and detail.description else f"Explore the {variant.model.manufacturer.name} {variant.model.name} {variant.year} available from Todde."),
		},
	}
	return render(request, "marketing/vehicle_detail.html", context)


@require_GET
def car_manufacturers_api(request):
	manufacturers = CarManufacturer.objects.filter(is_active=True).order_by("name")
	data = [
		{"id": manufacturer.id, "name": manufacturer.name, "slug": manufacturer.slug}
		for manufacturer in manufacturers
	]
	return JsonResponse({"manufacturers": data})


@require_GET
def car_models_api(request):
	manufacturer_id = request.GET.get("manufacturer")
	manufacturer_slug = request.GET.get("manufacturer_slug")
	if not manufacturer_id and not manufacturer_slug:
		return JsonResponse({"error": "Missing manufacturer parameter."}, status=400)

	manufacturer_filters = {"is_active": True}
	if manufacturer_id:
		manufacturer_filters["pk"] = manufacturer_id
	if manufacturer_slug:
		manufacturer_filters["slug"] = manufacturer_slug

	manufacturer = get_object_or_404(CarManufacturer, **manufacturer_filters)
	models = manufacturer.models.filter(is_active=True).order_by("name")
	data = [
		{"id": model.id, "name": model.name, "slug": model.slug}
		for model in models
	]
	return JsonResponse(
		{
			"manufacturer": {"id": manufacturer.id, "name": manufacturer.name, "slug": manufacturer.slug},
			"models": data,
		}
	)


@require_GET
def car_variants_api(request):
	model_id = request.GET.get("model")
	model_slug = request.GET.get("model_slug")
	if not model_id and not model_slug:
		return JsonResponse({"error": "Missing model parameter."}, status=400)

	model_filters = {"is_active": True, "manufacturer__is_active": True}
	if model_id:
		model_filters["pk"] = model_id
	if model_slug:
		model_filters["slug"] = model_slug

	model = get_object_or_404(CarModel, **model_filters)
	variants = model.variants.filter(is_active=True).order_by("-year", "trim")
	data = [
		{
			"id": variant.id,
			"year": variant.year,
			"trim": variant.trim,
			"price": str(variant.price),
			"currency": variant.currency,
			"formatted_price": variant.formatted_price,
		}
		for variant in variants
	]
	return JsonResponse(
		{
			"model": {
				"id": model.id,
				"name": model.name,
				"slug": model.slug,
				"manufacturer": {
					"id": model.manufacturer.id,
					"name": model.manufacturer.name,
					"slug": model.manufacturer.slug,
				},
			},
			"variants": data,
		}
	)


@require_GET
def search_api(request):
	query = request.GET.get("q", "").strip()
	
	if not query:
		return JsonResponse({"results": []})
	
	if len(query) < 2:
		return JsonResponse({"results": []})
	
	# Search across manufacturers, models, and variants
	results = []
	
	# Search manufacturers
	manufacturers = CarManufacturer.objects.filter(
		is_active=True,
		name__icontains=query
	).order_by("name")[:5]
	
	for manufacturer in manufacturers:
		results.append({
			"type": "manufacturer",
			"id": manufacturer.id,
			"title": manufacturer.name,
			"subtitle": "Manufacturer",
			"url": f"/cars/?manufacturer={manufacturer.slug}",
			"image": None
		})
	
	# Search models
	models = CarModel.objects.filter(
		is_active=True,
		manufacturer__is_active=True,
		name__icontains=query
	).select_related("manufacturer").order_by("name")[:5]
	
	for model in models:
		results.append({
			"type": "model",
			"id": model.id,
			"title": f"{model.manufacturer.name} {model.name}",
			"subtitle": "Model",
			"url": f"/cars/?model={model.slug}",
			"image": None
		})
	
	# Search variants (cars)
	variants = CarVariant.objects.filter(
		is_active=True,
		model__is_active=True,
		model__manufacturer__is_active=True
	).select_related("model", "model__manufacturer").prefetch_related(
		Prefetch(
			"images",
			queryset=CarVariantImage.objects.filter(is_active=True).order_by("order", "id"),
		)
	)
	
	# Filter variants by manufacturer name, model name, year, or trim
	from django.db.models import Q
	variant_filter = (
		Q(model__manufacturer__name__icontains=query) |
		Q(model__name__icontains=query) |
		Q(trim__icontains=query) |
		Q(year__icontains=query)
	)
	
	variants = variants.filter(variant_filter).order_by("-year", "model__manufacturer__name", "model__name")[:8]
	
	placeholder_image_url = static("images/vehicle-placeholder.svg")
	
	for variant in variants:
		# Get primary image
		image_info = _resolve_variant_primary_image(variant, placeholder_image_url)
		
		results.append({
			"type": "variant",
			"id": variant.id,
			"title": f"{variant.model.manufacturer.name} {variant.model.name} {variant.year}",
			"subtitle": f"{variant.trim} • {variant.formatted_price}",
			"url": f"/cars/{variant.id}/",
			"image": image_info.source_url if not image_info.is_placeholder else None
		})
	
	# Limit total results
	results = results[:10]
	
	return JsonResponse({"results": results})
