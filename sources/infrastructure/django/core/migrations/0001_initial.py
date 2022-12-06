# Generated by Django 4.1.3 on 2022-12-06 22:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TagORM",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("value", models.CharField(max_length=64, unique=True)),
            ],
            options={
                "db_table": "tag",
            },
        ),
        migrations.CreateModel(
            name="PollORM",
            fields=[
                (
                    "id",
                    models.CharField(max_length=256, primary_key=True, serialize=False),
                ),
                ("question", models.CharField(max_length=128)),
                (
                    "tags",
                    models.ManyToManyField(related_name="polls", to="core.tagorm"),
                ),
            ],
            options={
                "db_table": "poll",
            },
        ),
        migrations.CreateModel(
            name="AnswerORM",
            fields=[
                (
                    "id",
                    models.CharField(max_length=256, primary_key=True, serialize=False),
                ),
                ("value", models.CharField(max_length=128)),
                (
                    "poll",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="answers",
                        to="core.pollorm",
                    ),
                ),
            ],
            options={
                "db_table": "answer",
            },
        ),
    ]
