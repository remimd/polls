from django.db import models
from django.db.models import Model


class TagORM(Model):
    value = models.CharField(max_length=64, unique=True)

    class Meta:
        db_table = "tag"


class PollORM(Model):
    id = models.CharField(max_length=256, primary_key=True)
    question = models.CharField(max_length=128)
    tags = models.ManyToManyField(TagORM, related_name="polls")

    class Meta:
        db_table = "poll"


class AnswerORM(Model):
    id = models.CharField(max_length=256, primary_key=True)
    value = models.CharField(max_length=128)
    poll = models.ForeignKey(PollORM, models.CASCADE, related_name="answers")

    class Meta:
        db_table = "answer"
