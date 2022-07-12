from django.contrib import admin

from .models import Student


@admin.register(Student)
class AdminStudent(admin.ModelAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
    )
