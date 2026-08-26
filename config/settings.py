"""
Django settings for the portfolio project.

All environment-specific values are read from environment variables (see
.env.example) so nothing sensitive is hardcoded or committed to git.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in ("1", "true", "yes", "on")


def env_list(name, default=""):
    raw = os.environ.get(name, default)
    return [item.strip() for item in raw.split(",") if item.strip()]


# --- Core -------------------------------------------------------------
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-dev-only-key-change-me-in-production-1234567890",
)
DEBUG = env_bool("DEBUG", default=True)
ALLOWED_HOSTS = env_list("ALLOWED_HOSTS", "localhost,127.0.0.1")
CSRF_TRUSTED_ORIGINS = env_list("CSRF_TRUSTED_ORIGINS", "")

# Render sets this automatically to the service's *.onrender.com hostname —
# picking it up here means the free onrender.com URL works with no manual
# ALLOWED_HOSTS/CSRF_TRUSTED_ORIGINS edits. A later custom domain still
# needs to be added explicitly via the env vars above.
RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "").strip()
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
    CSRF_TRUSTED_ORIGINS.append(f"https://{RENDER_EXTERNAL_HOSTNAME}")

SITE_NAME = os.environ.get("SITE_NAME", "Prajin S | Portfolio")
SITE_DOMAIN = os.environ.get("SITE_DOMAIN", "localhost:8000")
SITE_URL = os.environ.get("SITE_URL", f"http://{SITE_DOMAIN}")

# Optional, used only if provided — the GitHub activity section hides
# itself gracefully when this is blank (see core/views.py).
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME", "").strip()

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.site_context",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# --- Database -----------------------------------------------------------
# SQLite for development. Set DATABASE_URL for a production database
# (e.g. postgres://user:pass@host:5432/dbname) — parsed only if present,
# so the project needs no extra dependency until you actually deploy.
DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()

if DATABASE_URL:
    from urllib.parse import urlparse

    parsed = urlparse(DATABASE_URL)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": parsed.path.lstrip("/"),
            "USER": parsed.username,
            "PASSWORD": parsed.password,
            "HOST": parsed.hostname,
            "PORT": parsed.port or 5432,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# --- Passwords ------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- i18n -----------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = os.environ.get("TIME_ZONE", "Asia/Kolkata")
USE_I18N = True
USE_TZ = True

# --- Static & media ---------------------------------------------------
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Admin-uploaded media (Profile photo/illustration, Project image/
# hero_image/screenshots) goes to local disk by default — fine in dev,
# and on any host with a persistent filesystem. Set Cloudinary credentials
# to move it to Cloudinary instead: required on hosts with an *ephemeral*
# filesystem (e.g. Render's free tier), where anything written to disk at
# runtime — including admin uploads — is wiped on the next deploy or
# restart.
#
# Two ways to provide credentials — either works:
#   1. Three separate vars (easier to paste correctly — no URL syntax to
#      get right): CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY,
#      CLOUDINARY_API_SECRET. Built into a CLOUDINARY_URL below.
#   2. A single CLOUDINARY_URL (cloudinary://<api_key>:<api_secret>@<cloud_name>),
#      if you already have that whole string from Cloudinary's dashboard.
# Either way, the constructed/given value is put back into the process
# environment: the cloudinary/cloudinary_storage packages read
# CLOUDINARY_URL from there themselves once it's set — no further config
# needed here.
CLOUDINARY_URL = os.environ.get("CLOUDINARY_URL", "").strip()
if not CLOUDINARY_URL:
    _cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME", "").strip()
    _api_key = os.environ.get("CLOUDINARY_API_KEY", "").strip()
    _api_secret = os.environ.get("CLOUDINARY_API_SECRET", "").strip()
    if _cloud_name and _api_key and _api_secret:
        CLOUDINARY_URL = f"cloudinary://{_api_key}:{_api_secret}@{_cloud_name}"
        os.environ["CLOUDINARY_URL"] = CLOUDINARY_URL
STORAGES = {
    "default": {
        "BACKEND": (
            "cloudinary_storage.storage.MediaCloudinaryStorage"
            if CLOUDINARY_URL
            else "django.core.files.storage.FileSystemStorage"
        ),
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
# Legacy mirror of STORAGES["staticfiles"] — some third-party packages
# (e.g. django-cloudinary-storage's collectstatic override) still read
# this directly rather than the STORAGES dict above. Deliberately NOT
# registering "cloudinary_storage" as an app (see MediaCloudinaryStorage
# below, used purely by import path) sidesteps that package's own
# collectstatic override entirely, but this stays as a harmless,
# future-proofing compatibility shim. STORAGES is what Django itself uses.
STATICFILES_STORAGE = STORAGES["staticfiles"]["BACKEND"]

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Where the downloadable resume PDF lives (see media/resume/README.md).
RESUME_FILE_NAME = os.environ.get("RESUME_FILE_NAME", "resume.pdf")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Email (contact form notifications) --------------------------------
EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", default=True)
CONTACT_NOTIFY_EMAIL = os.environ.get("CONTACT_NOTIFY_EMAIL", "")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "portfolio@example.com")

# --- Security (production hardening, only biting when DEBUG=False) -----
if not DEBUG:
    SECURE_SSL_REDIRECT = env_bool("SECURE_SSL_REDIRECT", default=True)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", "31536000"))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = "same-origin"
    X_FRAME_OPTIONS = "DENY"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}
