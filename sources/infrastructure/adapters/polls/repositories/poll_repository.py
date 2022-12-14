from asgiref.sync import sync_to_async
from django.db import transaction

from sources.domains.polls.entities import Answer, Poll
from sources.infrastructure.adapters.mixins.repositories import DjangoRepositoryMixin
from sources.infrastructure.django.core.models import AnswerORM, PollORM, TagORM


class PollRepository(DjangoRepositoryMixin):
    async def add(self, poll: Poll):
        return await sync_to_async(self._add)(poll)

    async def get(self, poll_id: str) -> Poll:
        return await sync_to_async(self._get)(poll_id)

    async def remove(self, poll_id: str):
        return await sync_to_async(self._remove)(poll_id)

    @transaction.atomic
    def _add(self, poll: Poll):
        poll_orm = PollORM.objects.create(id=poll.id, question=poll.question)

        if tag_values := tuple(poll.tag_values):
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

    def _get(self, poll_id: str) -> Poll:
        poll_orm = PollORM.objects.prefetch_related("answers", "tags").get(id=poll_id)
        answers_orm = poll_orm.answers.all()
        tags_orm = poll_orm.tags.all()

        poll = Poll.create(id=poll_orm.id, question=poll_orm.question)

        for answer_orm in answers_orm:
            answer = Answer.create(id=answer_orm.id, value=answer_orm.value)
            poll.add_answer(answer)

        for tag_orm in tags_orm:
            poll.add_tag(tag_orm.value)

        return poll

    def _remove(self, poll_id: str):
        deleted, _ = PollORM.objects.filter(id=poll_id).delete()

        if deleted == 0:
            raise PollORM.DoesNotExist(f"Poll with id: `{poll_id}` doesn't exist.")
