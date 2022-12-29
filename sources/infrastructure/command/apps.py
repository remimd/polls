from django.apps import AppConfig

from sources.infrastructure.command import module


class CommandConfig(AppConfig):
    label = "command"
    name = module
    verbose_name = "command"
