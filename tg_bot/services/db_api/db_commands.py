from asgiref.sync import sync_to_async
from django.shortcuts import get_object_or_404

from django_project.telegrambot.unitems.models import (
    Type,
    Discipline,
    Product,
    Purchace,
    ProductPurchase
)
from django_project.telegrambot.students.models import (
    Student,
)
from tg_bot.services.redis_db_cache import CACHE


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
def add_user(user_id, username, first_name, last_name):
    try:
        new_student = Student(
            id_user=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name
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
    return target.id
    # types = Product.objects.filter(discipline__name=item.name)


@sync_to_async
def add_to_cart(person, name, type_name):
    dis = get_object_or_404(
        Discipline,
        name=name
    )
    type_ = get_object_or_404(
        Type,
        name=type_name
    )
    product = get_object_or_404(
        Product,
        discipline=dis.id,
        type=type_.id
    )
    CACHE[person]["cart"].append(product)
    print(CACHE)


@sync_to_async
def packing(person, cart):
    user = get_object_or_404(
        Student,
        id_user=person
    )
    obj = Purchace.objects.create(
        buyer_id=user.id
    )
    for item in cart:
        products = ProductPurchase.objects.create(
            purchase=obj,
            product=item
        )
    # context = {
    #     "price": product.price,
    #     "target": obj
    # }
    # cart.clear()
    print(cart)
    return obj
