from django.db import models

from django_project.telegrambot.core.models import TimeBasedModel


class Student(TimeBasedModel):
    id_user = models.BigIntegerField(
        unique=True,
        verbose_name="ID пользователя Telegram"
    )
    username = models.CharField(
        max_length=250,
        verbose_name="Nickname пользователя"
    )
    first_name = models.CharField(
        max_length=150,
        null=True
    )
    last_name = models.CharField(
        max_length=150,
        null=True
    )

    class Meta:
        ordering = ("-id",)
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"

    def __str__(self):
        return f"ID - {self.id_user}, tg - @{self.username}"
