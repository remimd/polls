from abc import ABC
from typing import Type

from django.db.models import Model, Q, QuerySet


class DjangoRepositoryMixin(ABC):
    @staticmethod
    def is_unique_field(model: Type[Model], field: str) -> bool:
        attr = getattr(model, field)
        return attr.field.unique

    @staticmethod
    def get_by_values(model: Type[Model], field: str, *values) -> QuerySet:
        query = None

        for value in values:
            parameters = {field: value}
            current_query = Q(**parameters)
            query = query | current_query if query else current_query

        if query:
            return model.objects.filter(query)
        else:
            return model.objects.none()

    @classmethod
    def get_or_create_multiple(
        cls,
        model: Type[Model],
        unique_field: str,
        *values,
        **creation_params,
    ) -> list[Model]:
        if not cls.is_unique_field(model, unique_field):
            raise ValueError(f"Field `{unique_field}` isn't unique.")

        queryset = cls.get_by_values(model, unique_field, *values)
        existing = list(queryset)
        missing = []

        for value in values:
            for obj in existing:
                if value == getattr(obj, unique_field):
                    break
            else:
                parameters = creation_params | {unique_field: value}
                obj = model(**parameters)
                missing.append(obj)

        if missing:
            model.objects.bulk_create(missing)
            return existing + missing

        return existing
