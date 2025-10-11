from django.contrib import admin
from django.utils.html import format_html

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
	HomepageFinancingHighlight,
	HomepageFinancingStep,
	HomepageHero,
	HomepageSectionCopy,
	HomepageFeaturedVehicle,
	HomepageValueProposition,
	InventoryPageConfig,
	NavigationLink,
)


class CarVariantInline(admin.TabularInline):
	model = CarVariant
	extra = 1
	fields = ("year", "trim", "price", "currency", "is_active")
	show_change_link = True


class CarModelInline(admin.TabularInline):
	model = CarModel
	extra = 1
	fields = ("name", "is_active")
	show_change_link = True


class CarVariantImageInline(admin.TabularInline):
	model = CarVariantImage
	fields = ("image_preview", "image", "image_url", "alt_text", "order", "is_active")
	readonly_fields = ("image_preview",)
	extra = 1

	@admin.display(description="Preview")
	def image_preview(self, obj: CarVariantImage) -> str:
		if obj.pk and obj.source_url:
			return format_html(
				"<img src='{}' style='max-height: 80px;' alt='{}' />",
				obj.source_url,
				obj.alt_text or obj.variant,
			)
		return "–"


class CarVariantFeatureInline(admin.TabularInline):
	model = CarVariantFeature
	fields = ("text", "order", "is_active")
	extra = 1


class CarVariantSpecificationInline(admin.TabularInline):
	model = CarVariantSpecification
	fields = ("label", "value", "order", "is_active")
	extra = 1


@admin.register(CarManufacturer)
class CarManufacturerAdmin(admin.ModelAdmin):
	list_display = ("name", "is_active", "updated_at")
	list_filter = ("is_active",)
	search_fields = ("name",)
	prepopulated_fields = {"slug": ("name",)}
	inlines = [CarModelInline]


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
	list_display = ("name", "manufacturer", "is_active", "updated_at")
	list_filter = ("manufacturer", "is_active")
	search_fields = ("name", "manufacturer__name")
	prepopulated_fields = {"slug": ("name",)}
	inlines = [CarVariantInline]


@admin.register(CarVariant)
class CarVariantAdmin(admin.ModelAdmin):
	list_display = ("model", "year", "trim", "display_price", "is_active")
	list_filter = ("model__manufacturer", "model", "year", "is_active")
	search_fields = ("model__name", "model__manufacturer__name", "trim")
	autocomplete_fields = ("model",)
	ordering = ("-year", "model__manufacturer__name", "model__name")
	inlines = [CarVariantImageInline, CarVariantFeatureInline, CarVariantSpecificationInline]

	@admin.display(description="Price")
	def display_price(self, obj: CarVariant) -> str:
		return obj.formatted_price


@admin.register(CarVariantDetail)
class CarVariantDetailAdmin(admin.ModelAdmin):
	list_display = ("variant", "mileage_km", "location", "is_active", "updated_at")
	list_filter = ("is_active", "variant__model__manufacturer")
	search_fields = ("variant__model__name", "variant__model__manufacturer__name", "headline", "location")
	autocomplete_fields = ("variant",)
	ordering = ("-updated_at",)


@admin.register(NavigationLink)
class NavigationLinkAdmin(admin.ModelAdmin):
	list_display = ("label", "href", "order", "is_active")
	list_editable = ("order", "is_active")
	list_filter = ("is_active",)
	search_fields = ("label", "href")
	ordering = ("order", "label")


@admin.register(HomepageSectionCopy)
class HomepageSectionCopyAdmin(admin.ModelAdmin):
	list_display = ("slug", "heading", "is_active", "updated_at")
	list_filter = ("is_active",)
	search_fields = ("slug", "heading")
	ordering = ("slug",)


class OrderableAdmin(admin.ModelAdmin):
	list_display = ("__str__", "order", "is_active", "updated_at")
	list_editable = ("order", "is_active")
	list_filter = ("is_active",)
	ordering = ("order", "id")


@admin.register(HomepageHero)
class HomepageHeroAdmin(OrderableAdmin):
	search_fields = ("title", "badge_label")


@admin.register(HomepageCategory)
class HomepageCategoryAdmin(OrderableAdmin):
	search_fields = ("name", "description")


@admin.register(HomepageFeaturedVehicle)
class HomepageFeaturedVehicleAdmin(OrderableAdmin):
	autocomplete_fields = ("variant",)
	search_fields = ("name", "badge", "location")
	list_display = ("name", "badge", "order", "is_active", "updated_at")
	list_editable = ("order", "is_active")


@admin.register(HomepageValueProposition)
class HomepageValuePropositionAdmin(OrderableAdmin):
	search_fields = ("title", "description")


@admin.register(HomepageFinancingStep)
class HomepageFinancingStepAdmin(OrderableAdmin):
	search_fields = ("title", "description")


@admin.register(HomepageFinancingHighlight)
class HomepageFinancingHighlightAdmin(OrderableAdmin):
	search_fields = ("title", "description")


@admin.register(HomepageBrandMetric)
class HomepageBrandMetricAdmin(OrderableAdmin):
	search_fields = ("value", "label")


@admin.register(HomepageContactCard)
class HomepageContactCardAdmin(OrderableAdmin):
	search_fields = ("title", "description", "link_label")


@admin.register(InventoryPageConfig)
class InventoryPageConfigAdmin(admin.ModelAdmin):
	list_display = ("slug", "listing_type", "title", "is_active", "updated_at")
	list_filter = ("is_active", "listing_type")
	search_fields = ("title", "meta_title", "meta_description")
	ordering = ("slug",)


@admin.register(FinancingPageConfig)
class FinancingPageConfigAdmin(admin.ModelAdmin):
	list_display = ("slug", "hero_title", "is_active", "updated_at")
	list_filter = ("is_active",)
	search_fields = ("hero_title", "hero_subtitle", "corporate_heading")
	ordering = ("slug",)


@admin.register(FinancingSnapshotItem)
class FinancingSnapshotItemAdmin(OrderableAdmin):
	search_fields = ("text",)


@admin.register(FinancingBenefit)
class FinancingBenefitAdmin(OrderableAdmin):
	search_fields = ("title", "description")
