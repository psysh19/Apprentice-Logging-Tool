"""
Minimal Django settings for the Apprenticeship Activity Log.

This is a front-end-only build: no database, no models, no auth.
Only the pieces needed to render templates are switched on.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# For local development only. Generate a fresh key before any real deployment.
SECRET_KEY = "dev-only-not-secret-change-me"

DEBUG = True

ALLOWED_HOSTS = ["*"]

# Kept deliberately small. No auth/sessions/admin because nothing is stored yet.
INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "logbook",
]

MIDDLEWARE = [
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "logbook_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "logbook_project.wsgi.application"

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# How many activity pages to expose. Change this one number to add/remove pages.
ACTIVITY_PAGES = 10
