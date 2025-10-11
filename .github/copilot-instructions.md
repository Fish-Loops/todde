# todde Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-10-11

## Active Technologies
- Python 3.11 (Django officially supports 3.10–3.12; choose 3.11 for stability and async features). + Django 5.0 LTS, Django Rest Framework (for future API exposure), django-tailwind (or Tailwind CLI integration), django-allauth (existing auth), pytest-django, Playwright for visual regressions, axe-core CLI for accessibility scans. (001-todde-integrated-services)
- Python 3.11 (Django officially supports 3.10–3.12; choose 3.11 for stability and async features). + Django 5.0 LTS, Django Rest Framework (for future API exposure), django-tailwind (or Tailwind CLI integration), Flowbite (Tailwind component library) with Flowbite plugin, django-allauth (existing auth), pytest-django, Playwright for visual regressions, axe-core CLI for accessibility scans. (001-todde-integrated-services)
- PostgreSQL 15 for production (SQLite remains for local scaffolding). (001-todde-integrated-services)
- Python 3.11 (Django 5.0 LTS), TypeScript 5.x for frontend assets + Django, Django Rest Framework, Tailwind CSS + Flowbite, Vite, Style Dictionary, Celery 5, Redis, Pipenv for environment managemen (001-todde-integrated-services)
- PostgreSQL 15 (prod), SQLite for local scaffolding, Redis for task queue (001-todde-integrated-services)

## Project Structure
```
src/
tests/
```

## Commands
cd src [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] pytest [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] ruff check .

## Code Style
Python 3.11 (Django officially supports 3.10–3.12; choose 3.11 for stability and async features).: Follow standard conventions

## Recent Changes
- 001-todde-integrated-services: Added Python 3.11 (Django 5.0 LTS), TypeScript 5.x for frontend assets + Django, Django Rest Framework, Tailwind CSS + Flowbite, Vite, Style Dictionary, Celery 5, Redis, Pipenv for environment managemen
- 001-todde-integrated-services: Added Python 3.11 (Django officially supports 3.10–3.12; choose 3.11 for stability and async features). + Django 5.0 LTS, Django Rest Framework (for future API exposure), django-tailwind (or Tailwind CLI integration), Flowbite (Tailwind component library) with Flowbite plugin, django-allauth (existing auth), pytest-django, Playwright for visual regressions, axe-core CLI for accessibility scans.
- 001-todde-integrated-services: Added Python 3.11 (Django officially supports 3.10–3.12; choose 3.11 for stability and async features). + Django 5.0 LTS, Django Rest Framework (for future API exposure), django-tailwind (or Tailwind CLI integration), django-allauth (existing auth), pytest-django, Playwright for visual regressions, axe-core CLI for accessibility scans.

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
