import os

from django_project.telegrambot.students.models import Student
from django_project.telegrambot.unitems.models import Discipline, Product
from django.shortcuts import get_object_or_404
from asgiref.sync import sync_to_async


@sync_to_async
def select_user(user_id):
    student = get_object_or_404(
        Student,
        id=user_id
    )
    return student


@sync_to_async
def add_user(user_id, username):
    try:
        new_student = Student(
            id_user=user_id,
            username=username
        ).save()
        return new_student
    except Exception:
        return select_user(user_id)


@sync_to_async
def get_product(name):
    try:
        item = get_object_or_404(
            Discipline,
            name=name
        )
        context = {
            "target": item,
            "file": item.products.first().doc.path.split("/")[-1],
        }
        return context
    except Exception:
        return False


@sync_to_async
def file_(name):
    item = get_object_or_404(
        Discipline,
        name=name.upper()
    )
    return item.products.first().doc.path.split("/")[-1]


@sync_to_async
def get_types(name):
    item = get_object_or_404(
        Discipline,
        name=name.upper()
    )
    types = Product.objects.filter(discipline__name=item.name)
    return types


