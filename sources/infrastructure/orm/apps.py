from django.apps import AppConfig

from sources.infrastructure.orm import module


class ORMConfig(AppConfig):
    label = "orm"
    name = module
    verbose_name = "ORM"
