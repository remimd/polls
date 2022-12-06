import os


def setup_project():
    setup_django()


def setup_django():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "sources.infrastructure.django.settings",
    )
