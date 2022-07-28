from django.db import models

from django_project.telegrambot.students.models import Student

IDZ = "ИДЗ"
LR = "Л_Р"
LS = "лекции"
KR = "курсач"
K_R = "К_Р"

CHOICES = [
    (IDZ, 'Индивидуальное домашнее задание'),
    (LR, 'Лабораторная работа'),
    (LS, 'Лекции'),
    (KR, 'КР'),
    (K_R, 'контрольная'),
]


class Type(models.Model):
    name = models.CharField(
        max_length=150,
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
    name = models.CharField(
        max_length=200,
        verbose_name="Наименование дисциплины"
    )
    lektor = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="ФИО преподавателя"
    )
    consultation = models.EmailField(
        unique=True,
        blank=True,
        null=True,
        verbose_name="Консультация"
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Дисциплина"
        verbose_name_plural = "Дисциплины"

    def __str__(self):
        return self.name


def user_directory_path(instance, filename):
    # путь, куда будет осуществлена загрузка MEDIA_ROOT/.../<filename>
    return '{0}/{1}/{2}'.format(
        instance.discipline.name,
        instance.type.name,
        filename
    )


class Product(models.Model):
    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="дисциплина"
    )
    type = models.ForeignKey(
        Type,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="вид работы"
    )
    doc = models.FileField(
        upload_to=user_directory_path,
    )
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        verbose_name="Стоимость"
    )

    class Meta:
        ordering = ("-id",)
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"

    def __str__(self):
        return f"[{self.discipline.name}] - {self.type.name}"


class Purchace(models.Model):
    id = models.AutoField(
        primary_key=True,
        verbose_name="ID покупки"
    )
    buyer = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="purchaces"
    )
    item = models.ManyToManyField(
        to=Product,
        through="ProductPurchase",
        verbose_name="Продукт"
    )
    amount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        # null=True,
        # blank=True,
        verbose_name="Стоимость"
    )
    purchase_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время покупки"
    )
    successful = models.BooleanField(
        default=False,
        verbose_name="Состояние покупки"
    )

    class Meta:
        verbose_name = "Покупка"
        verbose_name_plural = "Покупки"

    def __str__(self):
        return "\n".join(
            (
                f"Номер заказа: {self.id}",
                f"Покупатель: {self.buyer.username}",
                f"Цена: {self.amount}"
            )
        )


class ProductPurchase(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    purchase = models.ForeignKey(
        Purchace,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"покупка {self.product}. {self.purchase}"
