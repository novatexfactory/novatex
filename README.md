NovaTex Factory — Wagtail/Django site

This repository contains the NovaTex Factory website built with Django and Wagtail.

Structure:
- `home/` — Wagtail page models and templates
- `templates/` — site templates
- `static/` — local static assets (CSS, JS, images)

To run locally:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
