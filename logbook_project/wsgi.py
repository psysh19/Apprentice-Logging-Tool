"""WSGI config for the logbook project."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "logbook_project.settings")

application = get_wsgi_application()
