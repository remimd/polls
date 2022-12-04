from django.apps import AppConfig

from sources.infrastructure.django.core import module as core_module


class CoreConfig(AppConfig):
    name = core_module
