"""Top-level URL routing. Everything lives in the logbook app."""

from django.urls import include, path

urlpatterns = [
    path("", include("logbook.urls")),
]
