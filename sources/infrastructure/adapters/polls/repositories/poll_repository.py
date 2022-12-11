from asgiref.sync import sync_to_async
from django.db import transaction

from sources.domains.polls.entities import Poll
from sources.infrastructure.adapters.mixins.repositories import DjangoRepositoryMixin
from sources.infrastructure.django.core.models import AnswerORM, PollORM, TagORM


class PollRepository(DjangoRepositoryMixin):
    async def add(self, poll: Poll):
        return await sync_to_async(self._add)(poll)

    @transaction.atomic
    def _add(self, poll: Poll):
        poll_orm = PollORM.objects.create(id=poll.id, question=poll.question)

        if tag_values := tuple(tag.value for tag in poll.tags):
            tags_orm = self.get_or_create_multiple(TagORM, "value", *tag_values)
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
