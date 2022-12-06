from sources.domains.polls.entities import Poll
from sources.infrastructure.django.core.models import AnswerORM, PollORM


class PollRepository:
    async def add(self, poll: Poll):
        poll_orm = await PollORM.objects.acreate(id=poll.id, question=poll.question)

        if answers := poll.answers:
            answers_orm = tuple(
                AnswerORM(
                    id=answer.id,
                    value=answer.value,
                    poll=poll_orm,
                )
                for answer in answers
            )
            await AnswerORM.objects.abulk_create(answers_orm)

        if tags := poll.tags:
            # TODO
            print(tags)
