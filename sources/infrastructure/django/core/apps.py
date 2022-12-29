from django.apps import AppConfig

from sources.infrastructure.django.core import module as core_module


class CoreConfig(AppConfig):
    label = "core"
    name = core_module
    verbose_name = "core"
