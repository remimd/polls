from django.db import models
from django.db.models import Model


""" ABSTRACT MODELS """


class EntityORM(Model):
    id = models.CharField(max_length=256, primary_key=True)

    class Meta:
        abstract = True


""" MODELS """


class TagORM(Model):
    value = models.CharField(max_length=64, unique=True)

    class Meta:
        db_table = "tag"


class PollORM(EntityORM):
    question = models.CharField(max_length=128)
    tags = models.ManyToManyField(TagORM, related_name="polls")

    class Meta:
        db_table = "poll"


class AnswerORM(EntityORM):
    value = models.CharField(max_length=128)
    poll = models.ForeignKey(PollORM, models.CASCADE, related_name="answers")

    class Meta:
        db_table = "answer"
