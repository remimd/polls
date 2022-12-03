import os

from dotenv import load_dotenv


def setup_project():
    load_dotenv()
    setup_django()


def setup_django():
    from sources.infrastructure.django.settings import module as django_settings_module

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", django_settings_module)
