from django.db import models


class TimeBasedModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Student(TimeBasedModel):
    id_user = models.BigIntegerField(
        unique=True,
        verbose_name="ID пользователя Telegram"
    )
    username = models.CharField(max_length=250)
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
