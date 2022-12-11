from abc import ABC
from typing import Type

from django.db.models import Model, Q, QuerySet


class DjangoRepositoryMixin(ABC):
    @staticmethod
    def is_unique_field(model: Type[Model], field: str):
        attribute = getattr(model, field)
        return attribute.field.unique or attribute.field.primary_key

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
        pk_or_unique_field: str,
        *values,
        **kwargs,
    ) -> list[Model]:
        if not cls.is_unique_field(model, pk_or_unique_field):
            raise ValueError(f"Field `{pk_or_unique_field}` isn't unique.")

        existing = list(cls.get_by_values(model, pk_or_unique_field, *values))
        missing = []

        for value in values:
            for obj in existing:
                if value == getattr(obj, pk_or_unique_field):
                    break
            else:
                parameters = kwargs | {pk_or_unique_field: value}
                obj = model(**parameters)
                missing.append(obj)

        if missing:
            model.objects.bulk_create(missing)

        return existing + missing
