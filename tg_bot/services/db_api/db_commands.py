from asgiref.sync import sync_to_async
from django_project.telegrambot.unitems.models import Product
from django_project.telegrambot.students.models import Student
from django.shortcuts import get_object_or_404


@sync_to_async()
def select_user(user_id: int):
    student = get_object_or_404(
        Student,
        id=user_id
    )
    return student

@sync_to_async
def add_user(user_id, username):
    try:
        Student(
            user_id=int(user_id),
            username=username
        ).save()
    except Exception:
        return select_user(user_id)
