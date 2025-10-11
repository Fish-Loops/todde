# Data Model – Todde Integrated Services Homepage & Financing Rebrand

## VehicleListing
- **Fields**:
  - `id` (UUID, primary key)
  - `slug` (SlugField, unique)
  - `make` (CharField, 64)
  - `model` (CharField, 64)
  - `trim` (CharField, 64, optional)
  - `year` (PositiveSmallIntegerField, 1990–current year +1)
  - `price_naira` (DecimalField, max_digits=12, decimal_places=2)
  - `thumbnail_image` (ForeignKey → `MarketingAsset`, required)
  - `gallery` (ManyToMany → `MarketingAsset`, blank=True)
  - `is_featured` (BooleanField)
  - `category` (ForeignKey → `VehicleCategory`)
  - `financing_program` (ForeignKey → `FinancingProgram`, null=True)
  - `hero_badge` (CharField, 32, choices: `"new"`, `"popular"`, `"limited"`, blank=True)
  - `financing_flags` (JSONField; default schema includes `down_payment_percent`, `eligibility_summary`)
  - `created_at` / `updated_at` (DateTimeField, auto-managed)
- **Relationships**: belongs to a `VehicleCategory`; optionally linked to a `FinancingProgram`; references curated `MarketingAsset` records for hero imagery.
- **Validation**: enforce `down_payment_percent == 30` when financing program flagged as Todde default; ensure price > 0; require accessible alt text on linked assets.

## VehicleCategory
- **Fields**:
  - `id` (UUID)
  - `name` (CharField, 32, unique)
  - `icon_asset` (ForeignKey → `MarketingAsset`)
  - `order` (PositiveSmallIntegerField)
- **Validation**: icon must include active/hover variants for Tailwind ring states.

## FinancingProgram
- **Fields**:
  - `id` (UUID)
  - `name` (CharField, unique)
  - `down_payment_percent` (DecimalField, default 30, validators 10–60)
  - `duration_months` (PositiveSmallIntegerField, choices: 12/18/24/36)
  - `apr_range` (CharField, pattern `"10-18"`)
  - `eligibility_requirements` (TextField)
  - `steps` (ArrayField of Step objects: `title`, `description`, `icon_asset`)
  - `status` (CharField, choices: `active`, `preview`, `retired`)
  - `created_at` / `updated_at`
- **State transitions**:
  - `preview → active` requires marketing approval timestamp
  - `active → retired` triggers deactivation of associated VehicleListing references
- **Validation**: enforce default 30% messaging in marketing copy; require eight steps for public financing flow.

## FinancingInquiry
- **Fields**:
  - `id` (UUID)
  - `vehicle` (ForeignKey → `VehicleListing`, null allowed for generic inquiries)
  - `full_name` (CharField, 128)
  - `email` (EmailField)
  - `phone_number` (PhoneNumberField, E.164)
  - `employment_status` (CharField, choices: employed/self-employed/other)
  - `monthly_income` (DecimalField)
  - `preferred_contact_time` (CharField, optional)
  - `status` (State: `submitted`, `contacted`, `in_review`, `approved`, `declined`)
  - `notes` (TextField, internal use)
  - `created_at` / `updated_at`
- **Validation**: capture consent checkbox, throttle submissions per IP/email, ensure automated email queued via Celery on `submitted`.

## MarketingAsset
- **Fields**:
  - `id` (UUID)
  - `slug` (SlugField)
  - `asset_type` (Enum: hero, thumbnail, icon, illustration)
  - `file` (ImageField)
  - `alt_text` (CharField, required)
  - `description` (TextField, optional)
  - `tone` (CharField, optional; e.g., `optimistic`, `trust`)
  - `breakpoint_variants` (JSONField listing mobile/tablet/desktop URLs)
  - `is_active` (BooleanField)
- **Validation**: alt text required; ensure variants exist for hero/banner assets; enforce palette compliance via manual review metadata.

## DesignTokenSnapshot
- **Fields**:
  - `id` (UUID)
  - `version` (SemVer string)
  - `source_file_hash` (CharField)
  - `payload` (JSONField with color/typography/spacing definitions)
  - `published_at` (DateTime)
- **Purpose**: track token updates, support rollback, and feed Tailwind build.

## Relationships Overview
- `VehicleListing` many-to-many with `MarketingAsset` for galleries; one-to-many with `FinancingInquiry`.
- `FinancingProgram` referenced by `VehicleListing` and provides default down payment messaging.
- `DesignTokenSnapshot` consumed by frontend build tasks; latest active snapshot exported to Tailwind theme.
- `MarketingAsset` reused by `VehicleCategory`, hero sections, financing banners, enforcing component-driven approach.

## Validation & Business Rules
- Alt text mandatory for all user-visible imagery (constitution Principle III).
- Default financing callouts must display "Pay 30% now" copy; any deviation requires governance approval flag.
- Pricing must include currency formatting and signage; ensure thousands separators.
- Submission confirmation triggers Celery task for email; on failure, surface toast and log audit trail.
- Data migrations should seed baseline tokens and assets; changes must update documentation and quickstart steps.
