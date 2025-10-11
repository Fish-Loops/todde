---
description: "Tracker-ready tickets for Todde Integrated Services Homepage & Financing Rebrand"
---

# Ticket Backlog – Todde Integrated Services Homepage & Financing Rebrand

This backlog converts the implementation tasks into tracker-ready tickets. Each entry includes a concise title, summary, acceptance criteria, dependencies, suggested estimate (story points), and labels.

> **Labels**: `todde-integrated-services`, `django`, `tailwind`, `flowbite`, `accessibility`, `celery`, `playwright`

## Phase 1 · Setup

### Ticket T001 · Bootstrap feature branch
- **Summary**: Ensure the feature branch `001-todde-integrated-services` exists, is up to date with `main`, and shared with the squad.
- **Acceptance Criteria**:
  - Branch created from latest `main`.
  - CI configured to target the branch.
  - Documentation updated with branch name reference.
- **Dependencies**: None
- **Estimate**: 1
- **Labels**: `setup`

### Ticket T002 · Backend environment ready
- **Summary**: Provision Poetry environment and install backend dependencies per quickstart.
- **Acceptance Criteria**:
  - `poetry install` completes without errors.
  - Lockfile checked for drift and committed if updated.
  - Documented verification instructions in `docs/development.md`.
- **Dependencies**: T001
- **Estimate**: 2
- **Labels**: `setup`, `python`

### Ticket T003 · Frontend dependencies installed
- **Summary**: Install Node dependencies in `frontend/` and verify tooling versions.
- **Acceptance Criteria**:
  - `npm install` completes successfully.
  - Node/Yarn/NPM versions recorded in dev docs.
  - Frontend lint command runs without fatal errors.
- **Dependencies**: T001
- **Estimate**: 2
- **Labels**: `setup`, `frontend`

### Ticket T004 · Style Dictionary + Tailwind wiring
- **Summary**: Configure Style Dictionary scripts and Tailwind/Flowbite plugins according to the plan.
- **Acceptance Criteria**:
  - `frontend/tailwind.config.js` updated with Flowbite plugin + Todde presets.
  - Style Dictionary build script generates CSS token artifacts.
  - Documentation describing overrides committed.
- **Dependencies**: T002, T003
- **Estimate**: 3
- **Labels**: `setup`, `design-system`

### Ticket T005 · Environment templates finished
- **Summary**: Draft `.env.example` including Postgres, Redis, AnyMail, and Vite URLs.
- **Acceptance Criteria**:
  - Template vetted with engineering + ops.
  - Comments describe required vs optional keys.
  - Secrets excluded from repo per constitution.
- **Dependencies**: T002
- **Estimate**: 2
- **Labels**: `setup`, `ops`

### Ticket T006 · Developer workflow documentation
- **Summary**: Capture dev server commands and concurrency expectations in `docs/development.md`.
- **Acceptance Criteria**:
  - Backend + frontend commands documented.
  - References quickstart for prerequisites.
  - Includes guidance for Celery worker + Playwright runs.
- **Dependencies**: T002, T003
- **Estimate**: 2
- **Labels**: `setup`, `docs`

## Phase 2 · Foundational

### Ticket T007 · Django app scaffolding
- **Summary**: Create skeleton apps `design_system`, `catalog`, `financing`, `marketing`.
- **Acceptance Criteria**:
  - Apps registered in Django settings.
  - `urls.py` files created with placeholders.
  - Basic tests verifying app loads.
- **Dependencies**: Phase 1 complete
- **Estimate**: 3
- **Labels**: `foundational`, `django`

### Ticket T008 · Design token pipeline
- **Summary**: Configure Style Dictionary to emit backend + frontend token artifacts and Flowbite overrides.
- **Acceptance Criteria**:
  - Generates `backend/apps/design_system/tokens.py` and `frontend/src/styles/tokens.css`.
  - Flowbite overrides stored in `frontend/src/styles/flowbite.overrides.css`.
  - Build step added to CI instructions.
- **Dependencies**: T004, T007
- **Estimate**: 5
- **Labels**: `design-system`, `foundational`

### Ticket T009 · Tailwind + Flowbite via Vite
- **Summary**: Integrate Tailwind/Flowbite assets through Vite bundler.
- **Acceptance Criteria**:
  - `frontend/vite.config.ts` outputs to `backend/static/dist`.
  - Flowbite init script in place.
  - Local build verified (`npm run build`).
- **Dependencies**: T003, T007
- **Estimate**: 5
- **Labels**: `frontend`, `foundational`

### Ticket T010 · Django static pipeline
- **Summary**: Update Django settings/templates to serve Vite-built bundles.
- **Acceptance Criteria**:
  - `settings/base.py` knows about Vite manifest.
  - `templates/base/base.html` loads compiled assets.
  - Collectstatic smoke test passes.
- **Dependencies**: T009
- **Estimate**: 3
- **Labels**: `django`, `foundational`

### Ticket T011 · Celery + Redis configuration
- **Summary**: Configure Celery, Redis, AnyMail, and stub financing email task.
- **Acceptance Criteria**:
  - Celery app defined with beat/worker settings.
  - Redis connection tested locally.
  - Financing email task enqueued from shell.
- **Dependencies**: T005, T007
- **Estimate**: 5
- **Labels**: `celery`, `backend`, `foundational`

### Ticket T012 · Marketing asset fixtures
- **Summary**: Seed baseline marketing asset fixtures.
- **Acceptance Criteria**:
  - Fixture JSON committed in `backend/apps/marketing/fixtures/`.
  - Load verified via `loaddata`.
  - Documentation listing asset keys.
- **Dependencies**: T007
- **Estimate**: 2
- **Labels**: `marketing`, `foundational`

### Ticket T013 · Accessibility testing harness
- **Summary**: Stand up Playwright + axe integration.
- **Acceptance Criteria**:
  - Playwright config stored under `tests/playwright/`.
  - Sample axe spec asserts homepage passes baseline.
  - GitHub Actions job outline prepared.
- **Dependencies**: T003, T007
- **Estimate**: 5
- **Labels**: `accessibility`, `foundational`, `testing`

## Phase 3 · US1 Discover Vehicles

### Ticket T014 · Vehicle categories data model
- **Summary**: Implement `VehicleCategory` model and admin registration.
- **Acceptance Criteria**:
  - Fields per data model with validations/tests.
  - Admin list filters configured.
  - Migration generated.
- **Dependencies**: T007
- **Estimate**: 3
- **Labels**: `us1`, `catalog`, `backend`

### Ticket T015 · Design system data models
- **Summary**: Implement `MarketingAsset` + `DesignTokenSnapshot` models.
- **Acceptance Criteria**:
  - Models + migrations generated.
  - Admin + serializer coverage.
  - Unit tests for snapshot retrieval.
- **Dependencies**: T007, T008
- **Estimate**: 3
- **Labels**: `us1`, `design-system`, `backend`

### Ticket T016 · US1 migrations rollout
- **Summary**: Generate and apply migrations for catalog + design system models.
- **Acceptance Criteria**:
  - Migrations run locally.
  - Recorded in release notes.
  - CI migration check passes.
- **Dependencies**: T014, T015
- **Estimate**: 2
- **Labels**: `us1`, `django`

### Ticket T017 · Featured listings service layer
- **Summary**: Build catalog service for hero payload + featured listings.
- **Acceptance Criteria**:
  - Service returns fixtures aligned with contracts.
  - Unit tests cover filtering + ordering.
  - Documented usage in view.
- **Dependencies**: T014, T015
- **Estimate**: 3
- **Labels**: `us1`, `backend`

### Ticket T018 · Public catalog API endpoints
- **Summary**: Implement API endpoints per `public-site.yaml`.
- **Acceptance Criteria**:
  - Django REST views/serializers created.
  - Contract tests verifying schema.
  - OpenAPI documentation regenerated.
- **Dependencies**: T017
- **Estimate**: 5
- **Labels**: `us1`, `api`, `backend`

### Ticket T019 · Homepage view composition
- **Summary**: Aggregate hero, value props, categories via marketing view.
- **Acceptance Criteria**:
  - View returns combined context object.
  - Integration test ensures data presence.
  - Cache strategy defined if needed.
- **Dependencies**: T017, T018
- **Estimate**: 3
- **Labels**: `us1`, `django`

### Ticket T020 · Homepage template implementation
- **Summary**: Build Flowbite-based homepage template.
- **Acceptance Criteria**:
  - Hero, categories, product grid, CTA laid out responsively.
  - Uses tokens, no inline color overrides.
  - Passes axe checks.
- **Dependencies**: T019, T021
- **Estimate**: 5
- **Labels**: `us1`, `frontend`, `templates`

### Ticket T021 · Homepage styles
- **Summary**: Implement Tailwind/Flowbite styles for homepage.
- **Acceptance Criteria**:
  - `home.css` + overrides committed.
  - Responsive breakpoints tested.
  - Linting passes.
- **Dependencies**: T004, T009
- **Estimate**: 3
- **Labels**: `us1`, `frontend`

### Ticket T022 · Category filter interactivity
- **Summary**: Build HTMX/Stimulus/Alpine interactions for category filters.
- **Acceptance Criteria**:
  - Filter updates grid without full page reload.
  - Focus states preserved.
  - Analytics hooks documented.
- **Dependencies**: T017, T021
- **Estimate**: 5
- **Labels**: `us1`, `frontend`, `interaction`

### Ticket T023 · Homepage routing + sitemap
- **Summary**: Wire homepage URL + sitemap entry.
- **Acceptance Criteria**:
  - URL resolves to marketing view.
  - Sitemap entry generated.
  - Tests confirm 200 response + canonical tag.
- **Dependencies**: T019, T020
- **Estimate**: 2
- **Labels**: `us1`, `django`

### Ticket T024 · Homepage fixture data
- **Summary**: Seed featured vehicles + hero copy fixtures.
- **Acceptance Criteria**:
  - Fixture JSON with categories + listings.
  - `loaddata` verifies.
  - Documented in README.
- **Dependencies**: T014
- **Estimate**: 2
- **Labels**: `us1`, `fixtures`

### Ticket T025 · US1 manual QA
- **Summary**: Validate homepage experience manually and record findings.
- **Acceptance Criteria**:
  - Loads under 3 seconds locally.
  - Visual QA notes captured with screenshots.
  - Accessibility checklist completed.
- **Dependencies**: T020–T024
- **Estimate**: 3
- **Labels**: `us1`, `qa`

## Phase 4 · US2 Financing Eligibility

### Ticket T026 · Financing models
- **Summary**: Implement `FinancingProgram` + `FinancingInquiry` models with admin + migrations.
- **Acceptance Criteria**:
  - Fields & constraints per data model.
  - Admin inline relationships configured.
  - Migrations pass.
- **Dependencies**: T007
- **Estimate**: 5
- **Labels**: `us2`, `backend`

### Ticket T027 · Financing service layer
- **Summary**: Build calculator logic, inquiry orchestration, Celery task call.
- **Acceptance Criteria**:
  - Service exposes calculator API.
  - Celery task invoked with validated payload.
  - Unit tests cover happy/edge cases.
- **Dependencies**: T026, T011
- **Estimate**: 5
- **Labels**: `us2`, `backend`, `celery`

### Ticket T028 · Financing API endpoints
- **Summary**: Implement endpoints per `financing.yaml` contract.
- **Acceptance Criteria**:
  - Serializer validation aligned with spec.
  - Contract tests verifying schema + HTTP codes.
  - Error handling documented.
- **Dependencies**: T027
- **Estimate**: 5
- **Labels**: `us2`, `api`

### Ticket T029 · Financing page view + template
- **Summary**: Assemble financing page view, forms, Flowbite template.
- **Acceptance Criteria**:
  - Renders hero, how-it-works steps, CTA.
  - Template uses design tokens.
  - Integration test ensures context completeness.
- **Dependencies**: T027, T028
- **Estimate**: 5
- **Labels**: `us2`, `frontend`, `django`

### Ticket T030 · Financing calculator interactivity
- **Summary**: Implement calculator TS module for dynamic updates/validation.
- **Acceptance Criteria**:
  - Handles default 30% message.
  - Edge cases logged + error states accessible.
  - Frontend tests or manual QA notes.
- **Dependencies**: T029
- **Estimate**: 3
- **Labels**: `us2`, `frontend`

### Ticket T031 · Inquiry confirmation UX
- **Summary**: Configure success banner tied to Celery status.
- **Acceptance Criteria**:
  - Success/error states displayed reliably.
  - Loading states accessible.
  - Celery responses surfaced in logs.
- **Dependencies**: T028, T030
- **Estimate**: 3
- **Labels**: `us2`, `frontend`, `celery`

### Ticket T032 · Financing fixtures
- **Summary**: Seed financing program steps + copy fixtures.
- **Acceptance Criteria**:
  - Fixture JSON stored under financing app.
  - Fixtures align with calculator assumptions.
  - QA instructions provided.
- **Dependencies**: T026
- **Estimate**: 2
- **Labels**: `us2`, `fixtures`

### Ticket T033 · Rate limiting + consent logging
- **Summary**: Add rate limiting middleware + consent checks.
- **Acceptance Criteria**:
  - Middleware throttles submissions beyond limits.
  - Consent captured in audit table/log.
  - Tests cover throttle + consent enforcement.
- **Dependencies**: T028
- **Estimate**: 5
- **Labels**: `us2`, `security`, `backend`

### Ticket T034 · US2 end-to-end smoke test
- **Summary**: Validate inquiry submission end-to-end.
- **Acceptance Criteria**:
  - Local run enqueues Celery task + logs h/t.
  - QA checklist completed.
  - Issues logged + assigned if found.
- **Dependencies**: T029–T033
- **Estimate**: 3
- **Labels**: `us2`, `qa`

## Phase 5 · US3 Trust & Support

### Ticket T035 · Marketing data extensions
- **Summary**: Extend marketing models for value props/testimonials.
- **Acceptance Criteria**:
  - Models + migrations created.
  - Admin + serializers exist.
  - Unit tests for content retrieval.
- **Dependencies**: T007
- **Estimate**: 3
- **Labels**: `us3`, `backend`

### Ticket T036 · Marketing content services
- **Summary**: Build service returning structured marketing content.
- **Acceptance Criteria**:
  - Service pulls from fixtures or CMS.
  - Tests ensure fallback when content missing.
  - Documented integration points.
- **Dependencies**: T035
- **Estimate**: 3
- **Labels**: `us3`, `backend`

### Ticket T037 · Value proposition module integration
- **Summary**: Integrate value props into homepage template using Flowbite cards.
- **Acceptance Criteria**:
  - Section responsive and accessible.
  - Data sourced from service.
  - Visual QA notes captured.
- **Dependencies**: T020, T036
- **Estimate**: 3
- **Labels**: `us3`, `frontend`

### Ticket T038 · Footer component
- **Summary**: Implement reusable footer partial with design tokens.
- **Acceptance Criteria**:
  - Partial included on homepage + financing.
  - Links accessible w/ focus styles.
  - Snapshot tests updated.
- **Dependencies**: T020, T029
- **Estimate**: 3
- **Labels**: `us3`, `frontend`, `templates`

### Ticket T039 · Trust fixtures
- **Summary**: Author testimonial/support fixtures.
- **Acceptance Criteria**:
  - Fixture JSON added under marketing app.
  - QA instructions to load fixtures.
  - Mapped to components.
- **Dependencies**: T035
- **Estimate**: 2
- **Labels**: `us3`, `fixtures`

### Ticket T040 · Footer accessibility audit
- **Summary**: Add Playwright + axe spec verifying footer accessibility.
- **Acceptance Criteria**:
  - Test resides in `tests/accessibility/footer.spec.ts`.
  - CI documentation updated.
  - Failing criteria triaged.
- **Dependencies**: T038, T013
- **Estimate**: 3
- **Labels**: `us3`, `accessibility`

### Ticket T041 · Support metadata updates
- **Summary**: Update sitemap + metadata with support info and structured data.
- **Acceptance Criteria**:
  - Sitemap entries include support endpoints.
  - Structured data validated via testing tool.
  - Documented in marketing handbook.
- **Dependencies**: T037, T038
- **Estimate**: 2
- **Labels**: `us3`, `seo`

## Phase 6 · Polish & Cross-Cutting

### Ticket T042 · Automated test suite run
- **Summary**: Execute pytest, Playwright, axe, Celery smoke tests.
- **Acceptance Criteria**:
  - Commands executed with passing status.
  - Logs attached to ticket.
  - Failures triaged if present.
- **Dependencies**: User stories complete
- **Estimate**: 3
- **Labels**: `polish`, `qa`

### Ticket T043 · Visual regression capture
- **Summary**: Capture before/after screenshots for homepage + financing.
- **Acceptance Criteria**:
  - Screenshots stored in `tests/visual/baselines/`.
  - Comparison script documented.
  - Linked in release notes.
- **Dependencies**: T020, T029
- **Estimate**: 3
- **Labels**: `polish`, `visual`

### Ticket T044 · Design system documentation update
- **Summary**: Update `docs/design-system.md` with Flowbite usage guidance.
- **Acceptance Criteria**:
  - New components documented.
  - Financing guidelines included.
  - PR includes content review sign-off.
- **Dependencies**: T020, T029, T037
- **Estimate**: 3
- **Labels**: `docs`, `design-system`

### Ticket T045 · Release changelog entry
- **Summary**: Draft changelog capturing token updates and feature highlights.
- **Acceptance Criteria**:
  - Entry covers US1–US3.
  - Stored in project changelog.
  - Reviewed by product & comms.
- **Dependencies**: T044
- **Estimate**: 2
- **Labels**: `docs`, `release`

### Ticket T046 · Brand & comms handoff
- **Summary**: Coordinate final copy/asset approval.
- **Acceptance Criteria**:
  - Meeting notes recorded.
  - Final copy merged.
  - Approval checklist signed.
- **Dependencies**: T043, T044
- **Estimate**: 3
- **Labels**: `polish`, `stakeholder`

### Ticket T047 · Deployment checklist
- **Summary**: Prepare deployment checklist covering collectstatic, CDN, email config.
- **Acceptance Criteria**:
  - Checklist stored in docs or ops runbook.
  - Includes rollback plan.
  - Reviewed with SRE/ops.
- **Dependencies**: T042, T045
- **Estimate**: 3
- **Labels**: `polish`, `release`
