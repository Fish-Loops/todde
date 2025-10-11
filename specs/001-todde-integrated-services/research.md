# Phase 0 Research – Todde Integrated Services Homepage & Financing Rebrand

## Decision: Use Vite-driven Tailwind build feeding Django static assets
- **Rationale**: Vite offers fast HMR for Tailwind, tree-shakes unused classes with the Django template extractor, and emits hashed bundles that Django can serve via `STATICFILES_STORAGE`. Keeps frontend tooling modern while preserving server-rendered templates.
- **Alternatives considered**:
  - `django-tailwind` management command: convenient but slower rebuilds and less control over PostCSS plugins; harder to share config with future micro-frontends.
  - Raw Tailwind CLI hooked into npm scripts: simple yet lacks dev server optimizations and requires extra scripting for asset hashing.

## Decision: Generate design tokens via Style Dictionary and sync to Tailwind + Django
- **Rationale**: Style Dictionary can ingest `tokens/design.json` and emit CSS variables, Tailwind theme extensions, and Python dictionaries. Ensures a single source of truth while keeping updates auditable.
- **Alternatives considered**:
  - Manual duplication of tokens in Tailwind config: risk of drift and violates constitution principle V.
  - Using Theo or custom scripts: heavier setup or more maintenance without clear benefit for current scale.

## Decision: Extend Flowbite with Todde design tokens
- **Rationale**: Flowbite provides accessible Tailwind components with ready JS behaviors; hooking into its plugin allows overriding color palette, spacing, and typography using the generated Style Dictionary output so components stay on-brand.
- **Alternatives considered**:
  - Building bespoke component library from scratch: higher effort and longer QA cycle, risking inconsistencies with Flowbite’s proven a11y patterns.
  - Using Headless UI exclusively: requires custom styling and JS for certain interactive components (modals, navigation), increasing scope.

## Decision: Pair Playwright with axe-core for automated accessibility regression
- **Rationale**: Playwright provides cross-browser coverage and screenshot diffing, while axe-core integrates via `@axe-core/playwright`, enabling automated WCAG 2.2 AA checks per constitution principle III.
- **Alternatives considered**:
  - Cypress + axe: comparable but adds another test runner alongside pytest; team already prefers Playwright for visual smoke tests.
  - Manual audits only: insufficient to guarantee regression coverage.

## Decision: Trigger financing inquiry emails via Celery worker using Django AnyMail
- **Rationale**: Celery with Redis broker decouples email sending from request latency, ensuring the on-page confirmation banner renders instantly while AnyMail standardizes ESP integrations.
- **Alternatives considered**:
  - Synchronous `send_mail`: simple but risks slower response times during ESP latency spikes (>500ms goal).
  - Django-Q/async tasks: lighter weight but less widely adopted; Celery aligns with broader Todde infra roadmap.

## Decision: Manage Python dependencies with Pipenv
- **Rationale**: Pipenv aligns with the team’s preferred workflow, providing deterministic `Pipfile.lock` management and virtualenv creation without introducing Poetry-specific tooling that contributors would need to learn.
- **Alternatives considered**:
  - Poetry: powerful but conflicts with explicit request to standardize on Pipenv and would duplicate dependency metadata.
  - Raw `pip` + requirements.txt: lacks built-in locking and virtualenv orchestration, increasing maintenance burden across services.
# Phase 0 Research – Todde Integrated Services Homepage & Financing Rebrand

## Decision: Use Vite-driven Tailwind build feeding Django static assets
- **Rationale**: Vite offers fast HMR for Tailwind, tree-shakes unused classes with the Django template extractor, and emits hashed bundles that Django can serve via `STATICFILES_STORAGE`. Keeps frontend tooling modern while preserving server-rendered templates.
- **Alternatives considered**:
  - `django-tailwind` management command: convenient but slower rebuilds and less control over PostCSS plugins; harder to share config with future micro-frontends.
  - Raw Tailwind CLI hooked into npm scripts: simple yet lacks dev server optimizations and requires extra scripting for asset hashing.

## Decision: Generate design tokens via Style Dictionary and sync to Tailwind + Django
- **Rationale**: Style Dictionary can ingest `tokens/design.json` and emit CSS variables, Tailwind theme extensions, and Python dictionaries. Ensures a single source of truth while keeping updates auditable.
- **Alternatives considered**:
  - Manual duplication of tokens in Tailwind config: risk of drift and violates constitution principle V.
  - Using Theo or custom scripts: heavier setup or more maintenance without clear benefit for current scale.

## Decision: Extend Flowbite with Todde design tokens
- **Rationale**: Flowbite provides accessible Tailwind components with ready JS behaviors; hooking into its plugin allows overriding color palette, spacing, and typography using the generated Style Dictionary output so components stay on-brand.
- **Alternatives considered**:
  - Building bespoke component library from scratch: higher effort and longer QA cycle, risking inconsistencies with Flowbite’s proven a11y patterns.
  - Using Headless UI exclusively: requires custom styling and JS for certain interactive components (modals, navigation), increasing scope.

## Decision: Pair Playwright with axe-core for automated accessibility regression
- **Rationale**: Playwright provides cross-browser coverage and screenshot diffing, while axe-core integrates via `@axe-core/playwright`, enabling automated WCAG 2.2 AA checks per constitution principle III.
- **Alternatives considered**:
  - Cypress + axe: comparable but adds another test runner alongside pytest; team already prefers Playwright for visual smoke tests.
  - Manual audits only: insufficient to guarantee regression coverage.

## Decision: Trigger financing inquiry emails via Celery worker using Django AnyMail
- **Rationale**: Celery with Redis broker decouples email sending from request latency, ensuring the on-page confirmation banner renders instantly while AnyMail standardizes ESP integrations.
- **Alternatives considered**:
  - Synchronous `send_mail`: simple but risks slower response times during ESP latency spikes (>500ms goal).
  - Django-Q/async tasks: lighter weight but less widely adopted; Celery aligns with broader Todde infra roadmap.
