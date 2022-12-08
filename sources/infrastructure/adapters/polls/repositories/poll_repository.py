from typing import Iterable

from asgiref.sync import sync_to_async
from django.db import transaction

from sources.domains.polls.entities import Poll
from sources.domains.polls.value_objects import Tag
from sources.infrastructure.django.core.models import AnswerORM, PollORM, TagORM


class PollRepository:
    async def add(self, poll: Poll):
        return await sync_to_async(self._add)(poll)

    @transaction.atomic
    def _add(self, poll: Poll):
        poll_orm = PollORM.objects.create(id=poll.id, question=poll.question)

        if tags_orm := self.bulk_get_or_create_tags(*poll.tags):
            poll_orm.tags.add(*tags_orm)

        if answers := poll.answers:
            answers_orm = tuple(
                AnswerORM(
                    id=answer.id,
                    value=answer.value,
                    poll=poll_orm,
                )
                for answer in answers
            )
            AnswerORM.objects.bulk_create(answers_orm)

    @staticmethod
    def bulk_get_or_create_tags(*tags: Tag) -> Iterable[TagORM]:
        values = tuple(tag.value for tag in tags)
        existing_tags = TagORM.objects.filter(value__in=values)

        if len(tags) == len(existing_tags):
            return existing_tags

        tags_orm = []
        missing_tags = []

        for tag in tags:
            for tag_orm in existing_tags:
                if tag.value != tag_orm.value:
                    continue

                tags_orm.append(tag_orm)
                break
            else:
                tag_orm = TagORM(value=tag.value)
                missing_tags.append(tag_orm)

        if missing_tags:
            TagORM.objects.bulk_create(missing_tags)

        return tags_orm + missing_tags
