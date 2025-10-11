# Quickstart – Todde Integrated Services Homepage & Financing Rebrand

## 1. Prerequisites
- Python 3.11
- Node.js 20.x + npm 10
- PostgreSQL 15 (local instance or Docker)
- Redis 7 (for Celery task queue)
- Pipenv 2023.x (dependency management)
- Playwright browsers installed (`npx playwright install`)

## 2. Clone & Branch
```bash
git checkout 001-todde-integrated-services
```

## 3. Backend Setup
```bash
pipenv install --dev
pipenv run python backend/manage.py migrate
pipenv run python backend/manage.py loaddata seeds/catalog.json seeds/marketing.json
```

## 4. Frontend (Tailwind + Vite)
```bash
cd frontend
npm install
npm install flowbite @headlessui/react --save
npm run dev    # watch mode for Tailwind/Vite
npm run build  # production build (outputs to ../backend/static/dist)
```

- Tailwind configuration extends tokens via `style-dictionary build` (see step 6) and registers `flowbite/plugin` with Todde overrides.
- Import Flowbite JS into `frontend/src/scripts/flowbite-init.ts` then reference bundle in Django base template.
- `vite.config.ts` proxies static references back to Django during development.

## 5. Run Servers Concurrently
```bash
# Terminal 1
pipenv run python backend/manage.py runserver 0.0.0.0:8000

# Terminal 2 (from frontend/)
npm run dev
```

- Access site at `http://localhost:8000` (Django serves templates, pulls dev assets via Vite proxy).

## 6. Sync Design Tokens
```bash
npm run tokens:build  # wraps style-dictionary build scripts
```
Outputs:
- `frontend/src/styles/tokens.css`
- `frontend/tailwind.config.js` theme extensions + Flowbite override config
- `backend/apps/design_system/tokens.py`
- `frontend/src/styles/flowbite.overrides.css`

## 7. Testing & Quality Gates
```bash
pipenv run pytest
pipenv run pytest --ds=backend.todde_backend.settings.dev backend/tests/accessibility
npx playwright test
npx playwright test --project=chromium --grep @axe
```

- Capture before/after screenshots using Playwright visual tests (`tests/visual/`).
- Ensure axe-core reports zero critical violations.

## 8. Celery Worker & Email Testing
```bash
pipenv run celery -A backend.todde_backend worker -l info
pipenv run python backend/manage.py shell -c "from financing.tasks import send_inquiry_email; send_inquiry_email.delay('test@example.com')"
npm run flowbite:build  # optional: regenerate Flowbite component bundle if overrides change
```

Configure `.env` with AnyMail provider (e.g., SendGrid) API key.

## 9. Documentation Updates
- Update `docs/design-system.md` with new component guidance.
- Record change log entry for token updates.

## 10. Deployment Checklist
- Run `npm run build && pipenv run python backend/manage.py collectstatic`.
- Verify hashed assets deployed to CDN.
- Execute smoke tests against staging environment (Playwright + axe) before release.
