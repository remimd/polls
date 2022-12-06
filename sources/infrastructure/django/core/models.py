from typing import Iterable

from django.db import models
from django.db.models import Model


class TagORM(Model):
    value: str = models.CharField(max_length=64, unique=True)

    class Meta:
        db_table = "tag"


class PollORM(Model):
    id: str = models.CharField(max_length=256, primary_key=True)
    question: str = models.CharField(max_length=128)
    tags: Iterable[TagORM] = models.ManyToManyField(TagORM, related_name="polls")

    class Meta:
        db_table = "poll"


class AnswerORM(Model):
    id: str = models.CharField(max_length=256, primary_key=True)
    value: str = models.CharField(max_length=128)
    poll: PollORM = models.ForeignKey(PollORM, models.CASCADE, related_name="answers")

    class Meta:
        db_table = "answer"
