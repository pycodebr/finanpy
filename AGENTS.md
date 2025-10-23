# Repository Guidelines

## Project Structure & Module Organization
Finanpy follows a classic Django layout. `core/` hosts global settings, URLs, and ASGI/WSGI entry points. Domain logic lives in app directories (`users/`, `profiles/`, `accounts/`, `categories/`, `transactions/`), each expected to expose `models.py`, `views.py`, `forms.py`, and `tests/`. Shared templates reside in `templates/`, static assets in `static/`, and Tailwind sources under `theme/static_src/` (compiled output is written to `theme/static/css/dist/`). Consult `docs/` for architecture, data models, and coding standards, and use `agents/` when invoking role-specific automation guidelines.

## Build, Test, and Development Commands
- `python manage.py runserver` — Start the development server at `http://127.0.0.1:8000`.
- `python manage.py makemigrations` / `python manage.py migrate` — Generate and apply schema changes; run both before shipping models.
- `python manage.py tailwind install` — Install or refresh Tailwind dependencies inside the `theme` app.
- `python manage.py tailwind start` — Watch Tailwind sources and rebuild CSS during UI work; use `python manage.py tailwind build` for a one-off production bundle.
- `python manage.py test` — Execute the Django test suite; add `--verbosity=2` when diagnosing failures.

## Coding Style & Naming Conventions
Adhere to the standards in `docs/coding-standards.md`: PEP 8 with four-space indentation, maximum 79-character lines (flex to 120 only when unavoidable), and single quotes for Python strings unless escaping demands otherwise. Keep names in English using `snake_case` for functions and variables, `PascalCase` for classes, and `UPPER_CASE` for constants. Group imports by standard library, Django, then local modules, each separated by a blank line. Templates should follow Tailwind’s utility-first approach and reuse layout blocks defined in `templates/base/`.

## Testing Guidelines
Place automated tests inside each app’s `tests/` package, splitting files by concern (`test_models.py`, `test_views.py`, etc.). Use Django’s `TestCase` plus fixtures or factories as apps mature. Aim for at least 80% coverage as outlined in `docs/coding-standards.md`, and keep tests deterministic by isolating user data per request. Run `python manage.py test accounts.tests.test_models` (or similar module-level targets) to iterate quickly before executing the full suite.

## Commit & Pull Request Guidelines
Follow the evolving Conventional Commit style visible in `git log`: `<type>: <imperative summary>` (e.g., `feat: adiciona dashboard inicial`). Keep summaries under 72 characters, and reference related tasks from `TASKS.md` or issue IDs in the body. Pull requests should include: a concise problem statement, the solution outline, test evidence (command output, coverage notes), and UI screenshots when templates change. Request at least one review from the relevant agent role (backend, frontend, QA, or product) before merging.

## Environment & Configuration Tips
Secrets live in `.env`; duplicate the template with `cp .env.example .env` and never commit local credentials. `python-decouple` reads configuration, so prefer `config('SETTING_NAME')` in `core/settings.py` instead of hard-coded values. SQLite is bundled for development, but confirm migrations before switching to production databases. Run `python manage.py collectstatic` prior to deploys so Tailwind assets land in `staticfiles/`.
