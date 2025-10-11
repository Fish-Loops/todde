# Implementation Plan: Todde Integrated Services Homepage & Financing Rebrand

**Branch**: `001-todde-integrated-services` | **Date**: 2025-10-11 | **Spec**: [`specs/001-todde-integrated-services/spec.md`](./spec.md)
**Input**: Feature specification from `/specs/001-todde-integrated-services/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Rebrand Todde’s public surfaces—homepage, financing flow, and trust content—using the shared design token system so every interaction reflects the updated palette, typography, and accessibility requirements. The work introduces Django apps for marketing, catalog, financing, and design system assets, compiles Tailwind + Flowbite styling via Vite, orchestrates financing inquiries through Celery, and relies on Pipenv for Python dependency management instead of Poetry.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.11 (Django 5.0 LTS), TypeScript 5.x for frontend assets  
**Primary Dependencies**: Django, Django Rest Framework, Tailwind CSS + Flowbite, Vite, Style Dictionary, Celery 5, Redis, Pipenv for environment management  
**Storage**: PostgreSQL 15 (prod), SQLite for local scaffolding, Redis for task queue  
**Testing**: pytest + pytest-django, Playwright, axe-core CLI, Django test client, frontend linting via ESLint  
**Target Platform**: Web (Django backend rendered HTML with Vite-built assets, deployed on Linux-based infrastructure)
**Project Type**: Web application with Django backend and standalone frontend build pipeline  
**Performance Goals**: Homepage LCP ≤ 3s on broadband, CLS < 0.1, Celery task latency < 2s for inquiry enqueue  
**Constraints**: Must satisfy WCAG 2.2 AA, reuse Todde tokens, maintain responsive behavior at 3 breakpoints, keep operational directories (.specify/.vscode/.github) out of git  
**Scale/Scope**: Supports 3 prioritized user stories (homepage MVP, financing flow, trust content) with future API exposure through DRF

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Visual identity alignment**: Plan leverages existing design tokens via Style Dictionary and Flowbite overrides—compliant.
- **Component-driven library**: Reuses and extends shared Django templates + Flowbite components rather than bespoke markup—compliant.
- **Accessibility**: Commits to axe-core + Playwright testing with reduced-motion support—compliant.
- **Governance**: Documentation updates scheduled for `docs/design-system.md` and design council sign-offs; .specify/.vscode/.github remain untracked per hygiene rule—compliant.
- **Workflow**: Includes discovery artifacts (plan/spec), automated validation, and documentation updates matching constitution requirements—compliant.

*Re-evaluated after Phase 1 outputs: research, data models, contracts, and quickstart align with constitution gates; no new violations introduced.*

## Project Structure

### Documentation (this feature)

```
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```
backend/
├── apps/
│   ├── catalog/
│   ├── design_system/
│   ├── financing/
│   └── marketing/
├── templates/
│   ├── base/
│   ├── includes/
│   └── pages/
├── static/
│   └── dist/                # Vite output artifact target
└── todde_backend/           # Django project settings & URLs

frontend/
├── src/
│   ├── scripts/
│   │   ├── flowbite-init.ts
│   │   ├── home-filter.ts
│   │   └── financing-calculator.ts
│   ├── styles/
│   │   ├── tokens.css
│   │   ├── home.css
│   │   ├── financing.css
│   │   └── flowbite.overrides.css
│   └── pages/
└── tests/
  └── accessibility/

tests/
├── playwright/
│   ├── axe.config.ts
│   └── footer.spec.ts
├── integration/
└── unit/
```

**Structure Decision**: Adopt the web-application split with Django backend and Vite-driven frontend bundle. New Django apps live under `backend/apps`, templates consolidate in `backend/templates`, and Vite outputs to `backend/static/dist` so Django can serve compiled assets. Frontend TypeScript + Tailwind sources reside in `frontend/src`, maintaining clear separation for tests and accessibility tooling.

## Complexity Tracking

*Fill ONLY if Constitution Check has violations that must be justified*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
