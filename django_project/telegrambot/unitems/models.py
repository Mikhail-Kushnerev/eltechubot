from django.db import models

IDZ = "Индивидуальное домашнее задание"
LR = "Лабораторная работа"
KR = "Курсовая работа"
K_R = "Контрольная работа"


CHOICES = [
    (IDZ, 'ИДЗ'),
    (LR, 'Л/Р'),
    (KR, 'КР'),
    (K_R, 'К/Р'),
]


class Type(models.Model):
    name = models.CharField(
        choices=CHOICES,
        unique=True,
        verbose_name="тип товара"
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "вид деятельности"
        verbose_name_plural = "виды деятельности"

    def __str__(self):
        return self.name


class Discipline(models.Model):
    name = models.CharField(max_length=200)
    lektor = models.CharField(max_length=200)

    class Meta:
        ordering = ["name"]
        verbose_name = "Дисциплина"
        verbose_name_plural = "Дисциплины"


class File(models.Model):
    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.CASCADE,
        related_name="files",
        verbose_name="дисциплина"
    )
    type = models.ForeignKey(
        Type,
        on_delete=models.CASCADE,
        related_name="files",
        verbose_name="вид работы"
    )
