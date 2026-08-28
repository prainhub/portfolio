"""
ASGI config for the portfolio project.

Exposes the ASGI callable as a module-level variable named ``application``.
For production, run behind a real ASGI server (uvicorn, daphne), e.g.:

    uvicorn config.asgi:application --host 0.0.0.0 --port 8000
"""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_asgi_application()
