from django.contrib import admin

from .models import (
    Product,
    Purchace,
    Type,
    Discipline
)


@admin.register(Type)
class AdminType(admin.ModelAdmin):
    list_display = (
        "name",
    )


@admin.register(Discipline)
class AdminDiscipline(admin.ModelAdmin):
    list_display = (
        "name",
        "lektor"
    )


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = (
        "discipline",
        "type",
    )


@admin.register(Purchace)
class AdminPurchace(admin.ModelAdmin):
    list_display = (
        'tg',
        'purchase_time',
        'id',
        'successful',
        'amount',
    )

    def tg(self, obj):
        return "@" + obj.buyer.username