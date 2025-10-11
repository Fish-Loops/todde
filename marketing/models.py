from __future__ import annotations

from django.db import models
from django.utils.text import slugify


class TimeStampedModel(models.Model):

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class OrderableModel(TimeStampedModel):
	order = models.PositiveIntegerField(default=0)

	class Meta:
		abstract = True
		ordering = ("order", "id")


class CarManufacturer(TimeStampedModel):

	name = models.CharField(max_length=120, unique=True)
	slug = models.SlugField(unique=True, max_length=140, blank=True)
	is_active = models.BooleanField(default=True)

	class Meta:
		ordering = ("name",)

	def save(self, *args, **kwargs):
		if not self.slug:
			base_slug = slugify(self.name)
			slug = base_slug or "manufacturer"
			counter = 1
			while CarManufacturer.objects.filter(slug=slug).exclude(pk=self.pk).exists():
				counter += 1
				slug = f"{base_slug}-{counter}" if base_slug else f"manufacturer-{counter}"
			self.slug = slug
		return super().save(*args, **kwargs)

	def __str__(self) -> str:
		return self.name


class CarModel(TimeStampedModel):
	class BodyType(models.TextChoices):
		SEDAN = ("sedan", "Sedan")
		SUV = ("suv", "SUV")
		COUPE = ("coupe", "Coupe")
		HATCHBACK = ("hatchback", "Hatchback")
		TRUCK = ("truck", "Truck")
		VAN = ("van", "Van")
		OTHER = ("other", "Other")

	manufacturer = models.ForeignKey(
		CarManufacturer,
		on_delete=models.CASCADE,
		related_name="models",
	)
	name = models.CharField(max_length=120)
	slug = models.SlugField(unique=True, max_length=160, blank=True)
	body_type = models.CharField(
		max_length=30,
		choices=BodyType.choices,
		default=BodyType.SEDAN,
	)
	is_active = models.BooleanField(default=True)

	class Meta:
		ordering = ("manufacturer__name", "name")
		unique_together = ("manufacturer", "name")

	def save(self, *args, **kwargs):
		if not self.slug:
			base_slug = slugify(self.name)
			slug = base_slug
			counter = 1
			while CarModel.objects.filter(slug=slug).exclude(pk=self.pk).exists():
				counter += 1
				slug = f"{base_slug}-{counter}"
			self.slug = slug
		return super().save(*args, **kwargs)

	def __str__(self) -> str:
		return f"{self.manufacturer.name} {self.name}"


class CarVariant(TimeStampedModel):
	class Transmission(models.TextChoices):
		AUTOMATIC = ("automatic", "Automatic")
		MANUAL = ("manual", "Manual")
		CVT = ("cvt", "CVT")
		DUAL_CLUTCH = ("dual-clutch", "Dual Clutch")
		OTHER = ("other", "Other")

	class ListingType(models.TextChoices):
		REGISTERED = ("registered", "Registered")
		FOREIGN_USED = ("foreign-used", "Foreign Used")

	model = models.ForeignKey(
		CarModel,
		on_delete=models.CASCADE,
		related_name="variants",
	)
	year = models.PositiveIntegerField()
	trim = models.CharField(max_length=120, blank=True)
	price = models.DecimalField(max_digits=12, decimal_places=2)
	currency = models.CharField(max_length=3, default="NGN")
	transmission = models.CharField(
		max_length=20,
		choices=Transmission.choices,
		default=Transmission.AUTOMATIC,
	)
	listing_type = models.CharField(
		max_length=20,
		choices=ListingType.choices,
		default=ListingType.REGISTERED,
	)
	is_active = models.BooleanField(default=True)

	class Meta:
		ordering = ("-year", "model__name")
		unique_together = ("model", "year", "trim")

	def __str__(self) -> str:
		trim_display = f" {self.trim}" if self.trim else ""
		return f"{self.model} {self.year}{trim_display}"

	@property
	def formatted_price(self) -> str:
		price_value = f"{self.price:,.0f}" if self.price == self.price.to_integral_value() else f"{self.price:,.2f}"
		return f"₦{price_value}" if self.currency.upper() == "NGN" else f"{self.currency} {price_value}"


class CarVariantDetail(TimeStampedModel):
	variant = models.OneToOneField(
		CarVariant,
		on_delete=models.CASCADE,
		related_name="detail",
	)
	headline = models.CharField(max_length=200, blank=True)
	subheadline = models.CharField(max_length=255, blank=True)
	description = models.TextField(blank=True)
	mileage_km = models.PositiveIntegerField(default=0)
	location = models.CharField(max_length=160, blank=True)
	finance_intro = models.CharField(max_length=255, blank=True)
	loan_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Annual interest rate percentage")
	loan_deposit_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Deposit percentage e.g. 30")
	loan_period_months = models.PositiveIntegerField(null=True, blank=True)
	applicant_types = models.CharField(max_length=255, blank=True, help_text="Comma separated list of applicant types")
	is_active = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Car variant detail"
		verbose_name_plural = "Car variant details"

	def __str__(self) -> str:
		return f"Details for {self.variant}"

	@property
	def applicant_type_choices(self) -> list[str]:
		if not self.applicant_types:
			return []
		return [item.strip() for item in self.applicant_types.split(",") if item.strip()]

	@property
	def mileage_display(self) -> str:
		return f"{self.mileage_km:,} km" if self.mileage_km else "—"


class CarVariantImage(OrderableModel):
	variant = models.ForeignKey(
		CarVariant,
		on_delete=models.CASCADE,
		related_name="images",
	)
	image_url = models.URLField()
	alt_text = models.CharField(max_length=160, blank=True)
	is_active = models.BooleanField(default=True)

	class Meta:
		ordering = ("order", "id")
		verbose_name = "Car variant image"
		verbose_name_plural = "Car variant images"

	def __str__(self) -> str:
		return f"Image for {self.variant}"


class CarVariantFeature(OrderableModel):
	variant = models.ForeignKey(
		CarVariant,
		on_delete=models.CASCADE,
		related_name="features",
	)
	text = models.CharField(max_length=255)
	is_active = models.BooleanField(default=True)

	class Meta:
		ordering = ("order", "id")
		verbose_name = "Car variant feature"
		verbose_name_plural = "Car variant features"

	def __str__(self) -> str:
		return self.text


class CarVariantSpecification(OrderableModel):
	variant = models.ForeignKey(
		CarVariant,
		on_delete=models.CASCADE,
		related_name="specifications",
	)
	label = models.CharField(max_length=160)
	value = models.CharField(max_length=255)
	is_active = models.BooleanField(default=True)

	class Meta:
		ordering = ("order", "id")
		verbose_name = "Car variant specification"
		verbose_name_plural = "Car variant specifications"

	def __str__(self) -> str:
		return f"{self.label}: {self.value}"


class NavigationLink(OrderableModel):
	label = models.CharField(max_length=120)
	href = models.CharField(max_length=255)
	description = models.CharField(max_length=255, blank=True)
	is_active = models.BooleanField(default=True)

	class Meta:
		ordering = ("order", "id")
		verbose_name = "Navigation link"
		verbose_name_plural = "Navigation links"

	def __str__(self) -> str:
		return self.label


class HomepageSectionCopy(TimeStampedModel):
	slug = models.SlugField(unique=True, max_length=80)
	heading = models.CharField(max_length=180, blank=True)
	subheading = models.CharField(max_length=255, blank=True)
	supporting_text = models.CharField(max_length=255, blank=True)
	cta_label = models.CharField(max_length=120, blank=True)
	cta_url = models.CharField(max_length=255, blank=True)
	is_active = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Homepage section copy"
		verbose_name_plural = "Homepage section copy"
		ordering = ("slug",)

	def __str__(self) -> str:
		return self.slug


class HomepageHero(OrderableModel):
	badge_label = models.CharField(max_length=120, blank=True)
	title = models.CharField(max_length=200)
	subtitle = models.TextField(blank=True)
	primary_cta_label = models.CharField(max_length=120, blank=True)
	primary_cta_url = models.CharField(max_length=255, blank=True)
	image_url = models.URLField(blank=True)
	is_active = models.BooleanField(default=True)

	class Meta:
		ordering = ("order", "id")
		verbose_name = "Homepage hero"
		verbose_name_plural = "Homepage heroes"

	def __str__(self) -> str:
		return self.title


class HomepageCategory(OrderableModel):
	name = models.CharField(max_length=120)
	icon = models.CharField(max_length=120)
	description = models.CharField(max_length=255, blank=True)
	is_active = models.BooleanField(default=True)

	class Meta:
		ordering = ("order", "id")
		verbose_name = "Homepage category"
		verbose_name_plural = "Homepage categories"

	def __str__(self) -> str:
		return self.name


class HomepageFeaturedVehicle(OrderableModel):
	variant = models.ForeignKey(
		CarVariant,
		on_delete=models.SET_NULL,
		related_name="featured_entries",
		null=True,
		blank=True,
	)
	name = models.CharField(max_length=180)
	price = models.CharField(max_length=120, blank=True)
	payment_plan = models.CharField(max_length=160, blank=True)
	image_url = models.URLField(blank=True)
	location = models.CharField(max_length=160, blank=True)
	badge = models.CharField(max_length=80, blank=True)
	is_active = models.BooleanField(default=True)

	class Meta:
		ordering = ("order", "id")
		verbose_name = "Homepage featured vehicle"
		verbose_name_plural = "Homepage featured vehicles"

	def __str__(self) -> str:
		return self.name

	@property
	def resolved_price(self) -> str:
		if self.price:
			return self.price
		if self.variant:
			return self.variant.formatted_price
		return ""

	@property
	def resolved_payment_plan(self) -> str:
		return self.payment_plan


class HomepageValueProposition(OrderableModel):
	title = models.CharField(max_length=160)
	description = models.TextField(blank=True)
	icon = models.CharField(max_length=120, blank=True)
	is_active = models.BooleanField(default=True)

	class Meta:
		ordering = ("order", "id")
		verbose_name = "Homepage value proposition"
		verbose_name_plural = "Homepage value propositions"

	def __str__(self) -> str:
		return self.title


class HomepageFinancingStep(OrderableModel):
	title = models.CharField(max_length=160)
	description = models.TextField(blank=True)
	is_active = models.BooleanField(default=True)

	class Meta:
		ordering = ("order", "id")
		verbose_name = "Homepage financing step"
		verbose_name_plural = "Homepage financing steps"

	def __str__(self) -> str:
		return self.title


class HomepageFinancingHighlight(OrderableModel):
	title = models.CharField(max_length=160)
	description = models.TextField(blank=True)
	is_active = models.BooleanField(default=True)

	class Meta:
		ordering = ("order", "id")
		verbose_name = "Homepage financing highlight"
		verbose_name_plural = "Homepage financing highlights"

	def __str__(self) -> str:
		return self.title


class HomepageBrandMetric(OrderableModel):
	value = models.CharField(max_length=40)
	label = models.CharField(max_length=160)
	is_active = models.BooleanField(default=True)

	class Meta:
		ordering = ("order", "id")
		verbose_name = "Homepage brand metric"
		verbose_name_plural = "Homepage brand metrics"

	def __str__(self) -> str:
		return f"{self.value} {self.label}"


class HomepageContactCard(OrderableModel):
	title = models.CharField(max_length=160)
	description = models.TextField(blank=True)
	link_label = models.CharField(max_length=120, blank=True)
	link_url = models.CharField(max_length=255, blank=True)
	is_active = models.BooleanField(default=True)

	class Meta:
		ordering = ("order", "id")
		verbose_name = "Homepage contact card"
		verbose_name_plural = "Homepage contact cards"

	def __str__(self) -> str:
		return self.title


class InventoryPageConfig(TimeStampedModel):
	class Slug(models.TextChoices):
		ALL = ("all", "All Cars")
		REGISTERED = ("registered", "Registered Cars")
		FOREIGN_USED = ("foreign-used", "Foreign Used Cars")

	slug = models.CharField(max_length=40, unique=True, choices=Slug.choices)
	listing_type = models.CharField(
		max_length=20,
		choices=CarVariant.ListingType.choices,
		blank=True,
	)
	title = models.CharField(max_length=180, blank=True)
	intro_text = models.TextField(blank=True)
	page_kicker = models.CharField(max_length=80, blank=True)
	summary_badge_label = models.CharField(max_length=120, blank=True)
	meta_title = models.CharField(max_length=200, blank=True)
	meta_description = models.TextField(blank=True)
	is_active = models.BooleanField(default=True)

	class Meta:
		ordering = ("slug",)
		verbose_name = "Inventory page configuration"
		verbose_name_plural = "Inventory page configurations"

	def __str__(self) -> str:
		return self.get_slug_display()

	def resolved_page_title(self, fallback: str) -> str:
		return self.title or fallback

	def resolved_intro(self, fallback: str) -> str:
		return self.intro_text or fallback

	def resolved_kicker(self, fallback: str) -> str:
		return self.page_kicker or fallback

	def resolved_summary_label(self, fallback: str) -> str:
		return self.summary_badge_label or fallback

	def resolved_meta_title(self, fallback: str) -> str:
		return self.meta_title or fallback

	def resolved_meta_description(self, fallback: str) -> str:
		return self.meta_description or fallback


class FinancingPageConfig(TimeStampedModel):
	class Slug(models.TextChoices):
		DEFAULT = ("financing", "Financing Page")

	slug = models.CharField(max_length=40, unique=True, choices=Slug.choices)
	hero_title = models.CharField(max_length=200, blank=True)
	hero_subtitle = models.TextField(blank=True)
	hero_primary_cta_label = models.CharField(max_length=120, blank=True)
	hero_primary_cta_url = models.CharField(max_length=255, blank=True)
	hero_secondary_cta_label = models.CharField(max_length=120, blank=True)
	hero_secondary_cta_url = models.CharField(max_length=255, blank=True)
	hero_background_image_url = models.URLField(blank=True)
	hero_callout_title = models.CharField(max_length=160, blank=True)
	hero_callout_text = models.CharField(max_length=255, blank=True)
	steps_heading = models.CharField(max_length=200, blank=True)
	steps_subheading = models.CharField(max_length=255, blank=True)
	benefits_heading = models.CharField(max_length=200, blank=True)
	benefits_subheading = models.CharField(max_length=255, blank=True)
	eligibility_heading = models.CharField(max_length=180, blank=True)
	eligibility_description = models.TextField(blank=True)
	eligibility_cta_label = models.CharField(max_length=160, blank=True)
	eligibility_cta_url = models.CharField(max_length=255, blank=True)
	testimonial_image_url = models.URLField(blank=True)
	testimonial_card_title = models.CharField(max_length=160, blank=True)
	testimonial_card_text = models.CharField(max_length=255, blank=True)
	corporate_heading = models.CharField(max_length=200, blank=True)
	corporate_subheading = models.CharField(max_length=255, blank=True)
	corporate_primary_cta_label = models.CharField(max_length=160, blank=True)
	corporate_primary_cta_url = models.CharField(max_length=255, blank=True)
	corporate_secondary_cta_label = models.CharField(max_length=160, blank=True)
	corporate_secondary_cta_url = models.CharField(max_length=255, blank=True)
	corporate_availability_heading = models.CharField(max_length=160, blank=True)
	corporate_availability_description = models.CharField(max_length=255, blank=True)
	is_active = models.BooleanField(default=True)

	class Meta:
		ordering = ("slug",)
		verbose_name = "Financing page configuration"
		verbose_name_plural = "Financing page configurations"

	def __str__(self) -> str:
		return self.get_slug_display()

	def resolve(self, field_name: str, fallback: str = "") -> str:
		value = getattr(self, field_name, "")
		return value or fallback


class FinancingSnapshotItem(OrderableModel):
	text = models.CharField(max_length=255)
	is_active = models.BooleanField(default=True)

	class Meta:
		ordering = ("order", "id")
		verbose_name = "Financing snapshot item"
		verbose_name_plural = "Financing snapshot items"

	def __str__(self) -> str:
		return self.text


class FinancingBenefit(OrderableModel):
	title = models.CharField(max_length=160)
	description = models.TextField(blank=True)
	icon = models.CharField(max_length=120, blank=True)
	is_active = models.BooleanField(default=True)

	class Meta:
		ordering = ("order", "id")
		verbose_name = "Financing benefit"
		verbose_name_plural = "Financing benefits"

	def __str__(self) -> str:
		return self.title

