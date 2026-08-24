"""
WSGI config for the portfolio project.

Exposes the WSGI callable as a module-level variable named ``application``.
For production, run behind a real WSGI server (gunicorn, uWSGI) — never
`manage.py runserver`. Example:

    gunicorn config.wsgi:application --bind 0.0.0.0:8000
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()
