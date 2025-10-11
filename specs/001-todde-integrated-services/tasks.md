---
description: "Task list for Todde Integrated Services Homepage & Financing Rebrand"
---

# Tasks: Todde Integrated Services Homepage & Financing Rebrand

**Input**: Design documents from `/specs/001-todde-integrated-services/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Not explicitly mandated in the spec. Include targeted verifications only where required for acceptance.

**Organization**: Tasks are grouped by user story (US1–US3) to ensure each slice is independently implementable and testable.

## Format: `[ID] [P?] [Story] Description`
- **[P]**: Task can run in parallel (no shared files/dependencies)
- **[Story]**: User story label (US1, US2, US3)
- Provide absolute or clearly rooted file paths

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare tooling, environments, and repo scaffolding referenced by all stories.

- [ ] T001 [P] [Setup] Ensure branch `001-todde-integrated-services` is checked out and synced (git).
- [ ] T002 [P] [Setup] Provision Poetry environment and install backend dependencies (`poetry install`).
- [ ] T003 [P] [Setup] Install Node dependencies in `frontend/` (`npm install`).
- [ ] T004 [P] [Setup] Configure Style Dictionary scripts and Tailwind/Flowbite plugin wiring in `frontend/tailwind.config.js` per plan.
- [ ] T005 [P] [Setup] Set up environment templates (`.env.example`) covering Postgres, Redis, AnyMail credentials, and Vite URLs.
- [ ] T006 [P] [Setup] Document dev server commands and concurrency expectations inside `docs/development.md` (reference quickstart).

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that must exist before any user story work begins.

- [ ] T007 [Foundational] Establish Django app skeletons (`backend/apps/design_system`, `catalog`, `financing`, `marketing`) with `__init__.py`, `apps.py`, and basic urls.
- [ ] T008 [Foundational] Implement design token pipeline: configure Style Dictionary build to generate `backend/apps/design_system/tokens.py`, `frontend/src/styles/tokens.css`, and Flowbite overrides.
- [ ] T009 [Foundational] Integrate Tailwind + Flowbite asset build via Vite: update `frontend/vite.config.ts`, create `frontend/src/scripts/flowbite-init.ts`, ensure output to `backend/static/dist`.
- [ ] T010 [Foundational] Configure Django static settings and template loaders to consume Vite-built bundles (update `backend/todde_backend/settings/base.py` and `templates/base/base.html`).
- [ ] T011 [Foundational] Set up Celery with Redis, AnyMail provider configuration, and stub financing email task (`backend/apps/financing/tasks.py`).
- [ ] T012 [P] [Foundational] Seed baseline marketing assets and tokens fixtures (`backend/apps/marketing/fixtures/initial_assets.json`).
- [ ] T013 [Foundational] Establish accessibility testing harness using Playwright + axe (`tests/playwright/axe.config.ts`, sample spec).

**Checkpoint**: Foundation ready – user stories can commence.

---

## Phase 3: User Story 1 – Discover vehicles with Todde-branded experience (Priority P1) 🎯 MVP

**Goal**: Deliver a fully branded homepage showcasing hero content, categories, and product grid with responsive + accessible behavior.

**Independent Test**: Load homepage (desktop + mobile emulation) and validate hero, navigation, categories, and product grid align with Todde design tokens and respond to filter interactions.

### Implementation Tasks

- [ ] T014 [P] [US1] Implement `VehicleCategory` model + admin registrations in `backend/apps/catalog/models.py` (fields & validations from data-model.md).
- [ ] T015 [P] [US1] Implement `MarketingAsset` and `DesignTokenSnapshot` models in `backend/apps/design_system/models.py`.
- [ ] T016 [US1] Create migrations for catalog/design_system apps and run locally.
- [ ] T017 [P] [US1] Build catalog service layer for featured listings and hero payload (`backend/apps/catalog/services/listings.py`).
- [ ] T018 [US1] Implement public catalog API endpoints per `contracts/public-site.yaml` (`backend/apps/catalog/api.py`, `urls.py`).
- [ ] T019 [US1] Create homepage view + context in `backend/apps/marketing/views/home.py` to aggregate hero/value props/categories.
- [ ] T020 [US1] Construct homepage template using Flowbite components (`backend/templates/pages/home.html`), ensuring hero, categories, product grid, and CTA structure.
- [ ] T021 [P] [US1] Implement Tailwind/Flowbite styles for homepage (update `frontend/src/styles/home.css`, `flowbite.overrides.css`).
- [ ] T022 [P] [US1] Add interactive category filter behavior with HTMX/Stimulus or Alpine JS (`frontend/src/scripts/home-filter.ts`, hook into Flowbite states).
- [ ] T023 [US1] Wire homepage route in `backend/todde_backend/urls.py` and add sitemap entry.
- [ ] T024 [P] [US1] Prepare fixture data for featured vehicles & hero marketing copy (`backend/apps/catalog/fixtures/featured_listings.json`).
- [ ] T025 [US1] Manual QA: verify hero copy renders within 3 seconds, categories highlight with Todde orange ring, product grid responsive breakpoints maintain layout.

**Checkpoint**: US1 independently functional and demoable.

---

## Phase 4: User Story 2 – Evaluate financing eligibility (Priority P2)

**Goal**: Present financing explainer page with Flowbite-driven components, updated hero, how-it-works steps, calculator, and inquiry submission tied to Celery email confirmation.

**Independent Test**: Navigate directly to financing page, confirm content structure, adjust calculator inputs (fixed 30% messaging), submit inquiry, observe on-page confirmation and email queue status.

### Implementation Tasks

- [ ] T026 [P] [US2] Implement `FinancingProgram` and `FinancingInquiry` models (fields/states per data-model.md) with admin + migrations (`backend/apps/financing/models.py`).
- [ ] T027 [US2] Build financing services: calculator logic, inquiry submission orchestration, Celery task invocation (`backend/apps/financing/services/eligibility.py`).
- [ ] T028 [US2] Implement financing API endpoints from `contracts/financing.yaml` (`backend/apps/financing/api.py`, serializers).
- [ ] T029 [US2] Create financing page view, forms, and Flowbite-based template (`backend/apps/financing/views/page.py`, `templates/pages/financing.html`).
- [ ] T030 [P] [US2] Develop frontend script for calculator interactivity and validation (`frontend/src/scripts/financing-calculator.ts`).
- [ ] T031 [US2] Configure confirmation banner UX and tie to Celery-triggered email status (update template + JS to show success/error).
- [ ] T032 [P] [US2] Seed financing program steps and default 30% copy fixtures (`backend/apps/financing/fixtures/programs.json`).
- [ ] T033 [US2] Add rate limiting and consent checks in inquiry handler, logging audit trail (`backend/apps/financing/middleware/rate_limit.py`).
- [ ] T034 [US2] Smoke-test inquiry submission end-to-end (local) ensuring email queue receives job.

**Checkpoint**: US1 + US2 functional; financing flows independently verifiable.

---

## Phase 5: User Story 3 – Access trust and support information (Priority P3)

**Goal**: Reinforce credibility with value proposition, testimonials, footer, and support content across site using design-system components.

**Independent Test**: Scroll value proposition + footer sections; confirm icons, copy, and contact info align with brand tokens and accessibility guidelines.

### Implementation Tasks

- [ ] T035 [P] [US3] Extend marketing CMS data structures for value props/testimonials (`backend/apps/marketing/models.py`).
- [ ] T036 [US3] Build marketing content service pulling data from fixtures or CMS endpoint (`backend/apps/marketing/services/content.py`).
- [ ] T037 [US3] Integrate value proposition module into homepage template (reuse Flowbite cards) with copy from service.
- [ ] T038 [US3] Implement footer component partial leveraging design tokens (`backend/templates/includes/footer.html`).
- [ ] T039 [P] [US3] Author fixtures for testimonials/support contacts (`backend/apps/marketing/fixtures/testimonials.json`).
- [ ] T040 [US3] Audit accessibility: ensure footer links, icons meet contrast + focus states (`tests/accessibility/footer.spec.ts`).
- [ ] T041 [US3] Update sitemap and metadata to include support contact info (structured data if required).

**Checkpoint**: All user stories deliver independently testable experiences.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: End-to-end refinements, documentation, and release readiness.

- [ ] T042 [P] Run full automated suite: pytest, Playwright, axe, Celery worker smoke tests (reference quickstart).
- [ ] T043 [P] Capture before/after screenshots for homepage & financing (desktop + mobile) and store in `tests/visual/baselines/`.
- [ ] T044 Update `docs/design-system.md` with new Flowbite component usage, financing guidelines, and hero messaging rules.
- [ ] T045 Draft change log entry summarizing design token updates and feature release notes.
- [ ] T046 Coordinate handoff with Brand & Communications for final copy and asset approval; document sign-off in project wiki.
- [ ] T047 Prepare deployment checklist: ensure `collectstatic`, CDN invalidation, and email provider config validated.

---

## Dependencies & Execution Order

1. **Phase 1 → Phase 2**: Setup must complete before foundational tasks.
2. **Phase 2 → Phases 3-5**: Foundational tasks block all user stories.
3. **User Stories**: US1 (P1) is MVP; US2 & US3 may run in parallel once Phase 2 finishes, provided team capacity and data dependencies (e.g., marketing assets) are ready.
4. **Phase 6** depends on completion of selected user stories.

### Story Dependency Graph

- US1 (P1) → foundational requirement for brand consistency.
- US2 (P2) depends on foundational tasks plus shared design tokens but not on US1 deliverables (can parallel).
- US3 (P3) depends on foundational tasks; optionally consumes marketing assets defined during US1 but can proceed independently with fixtures.

### Parallel Opportunities

- Setup tasks T001–T006 are parallel.
- Foundational tasks T008, T012, T013 can run parallel after T007.
- Within US1: T014/T015/T017/T021/T022/T024 parallelizable.
- Within US2: T026/T030/T032 in parallel; T027 → T028 sequential; T029 parallel with T030 once models exist.
- Within US3: T035, T039 parallel; T037 depends on T036.

---

## Implementation Strategy

- **MVP**: Complete Phases 1–3 (through US1) to deliver branded homepage.
- **Incremental Delivery**: Add US2 for financing experience, then US3 for trust content.
- **Quality Gates**: Execute automated suites (T042) and visual audits (T043) before release.
- **Documentation**: Keep design system artifacts and quickstart instructions in sync (T044, T045).

---
