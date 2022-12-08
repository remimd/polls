import os


def setup_project():
    from .django import asgi  # noqa

    setup_django()
    setup_controllers()


def setup_controllers():
    from .api import controllers  # noqa


def setup_django():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "sources.infrastructure.django.settings",
    )
