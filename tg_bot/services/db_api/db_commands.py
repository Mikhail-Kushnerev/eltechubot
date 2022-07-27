import os

from django_project.telegrambot.students.models import Student
from django_project.telegrambot.unitems.models import (
    Discipline,
    Product,
    Purchace,
    ProductPurchase
)
from django_project.telegrambot.students.models import (
    Student,
)
from django.shortcuts import get_object_or_404
from asgiref.sync import sync_to_async



@sync_to_async
def get_student(user_id):
    student = get_object_or_404(
        Student,
        id=user_id
    )
    return True if student else False


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
def get_types(name):
    item = get_object_or_404(
        Discipline,
        name=name.upper()
    )
    types = Product.objects.filter(discipline__name=item.name)
    return types


@sync_to_async
def get_item(dis, type_name):
    target = get_object_or_404(
        Product,
        item=dis.id,
        type=type_name.id
    )
    return target
    # types = Product.objects.filter(discipline__name=item.name)


@sync_to_async
def add_to_cart(person, name):
    obj = Purchace.objects.create(
        buyer_id=person,
        # item=pk,
        # amount=5,
    ).save()
    product = get_object_or_404(
        Product,
        name=name
    )
    target = get_item(product)
    products = ProductPurchase.objects.create(
        purchase=obj.id,
        product=target
    )
    return obj
