from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.db.models import Model
from phonenumber_field.modelfields import PhoneNumberField


""" ABSTRACT MODELS """


class EntityORM(Model):
    id = models.CharField(max_length=256, primary_key=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ("id",)


""" MODELS """


class UserORM(AbstractBaseUser, EntityORM):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    phone = PhoneNumberField(unique=True, blank=True, null=True)

    USERNAME_FIELD = "email"

    class Meta:
        db_table = "user"
        verbose_name = "user"


class TagORM(Model):
    value = models.CharField(max_length=64, unique=True)

    class Meta:
        db_table = "tag"
        verbose_name = "tag"


class PollORM(EntityORM):
    question = models.CharField(max_length=128)
    tags = models.ManyToManyField(TagORM, related_name="polls")

    class Meta:
        db_table = "poll"
        verbose_name = "poll"


class AnswerORM(EntityORM):
    value = models.CharField(max_length=128)
    poll = models.ForeignKey(PollORM, models.CASCADE, related_name="answers")

    class Meta:
        db_table = "answer"
        verbose_name = "answer"
