# Todde Integrated Services Web Experience

A Django-driven marketing site for Todde Integrated Services featuring a branded homepage and car financing flow. Styling is powered by Tailwind CSS and Flowbite, aligned with the Todde brand guide.

## Prerequisites

- Python 3.12+
- pipenv (or your preferred virtual environment manager)
- Node.js 18+

## Setup

```bash
# Install Python dependencies
pipenv install --dev

# Activate the virtual environment
pipenv shell

# Run database migrations (SQLite by default)
python manage.py migrate
```

## Frontend assets

Tailwind CSS builds are managed with npm scripts defined in `package.json`.

```bash
# Install Node dependencies
npm install

# Build production CSS
npm run build:css

# Or run a local watcher during development
npm run dev:css
```

The compiled stylesheet is written to `static/css/todde.css`. Flowbite assets are vendored into `static/js/flowbite.min.js`.

## Local development

```bash
# Start the Django development server
python manage.py runserver
```

Visit <http://127.0.0.1:8000/> to explore the homepage and <http://127.0.0.1:8000/financing/> for the financing experience.

## Testing

```bash
python manage.py test
```

## Project structure highlights

- `marketing/` — Django app hosting marketing views, templates, and template tags.
- `templates/` — Global base template plus shared partials.
- `assets/css/todde.css` — Tailwind CSS source file.
- `static/` — Compiled CSS, Flowbite JS bundle, and brand assets (e.g., favicon).
- `tailwind.config.js` — Tailwind theme tokens aligned with the Todde brand palette.

## Accessibility & performance

- Color palette and typography adhere to the Todde brand document.
- Buttons, links, and cards include focus styles and hover transitions.
- Layout scales across breakpoints (1366 / 1024 / 768 / 480) per requirements.

Feel free to adapt the static data in `marketing/content.py` when integrating with live APIs or a CMS.
