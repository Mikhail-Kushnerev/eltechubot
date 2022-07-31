import decimal

from aiogram.utils import markdown
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


@sync_to_async
def info_func(dis_id: int) -> str:
    item = Discipline.objects.get(id=dis_id)
    return item.consultation


@sync_to_async
def get_student(user_id: int) -> bool:
    student: Student = get_object_or_404(
        Student,
        id=user_id
    )
    return True if student else False


@sync_to_async
def add_user(
        user_id: int,
        username: str,
        first_name: str,
        last_name: str
) -> str:
    try:
        if Student.objects.get(
                id_user=user_id
        ):
            text: str = "Введи интересующую тебя дисциплину. Возможно, она у меня есть"
        else:
            raise Exception
    except Exception:
        Student.objects.create(
            id_user=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        text: str = "".join(
            (
                "Спсибо за регистрацию, ",
                markdown.hbold("студент")
            )
        )
    finally:
        return text


@sync_to_async
def get_product(name: str):
    item: Discipline = get_object_or_404(
        Discipline,
        name=name
    )
    return item


@sync_to_async
def find_type(type_name: str) -> Type:
    result: Type = get_object_or_404(
        Type,
        name=type_name
    )
    return result


@sync_to_async
def get_types(name: str) -> Purchace:
    item: Discipline = get_object_or_404(
        Discipline,
        name=name.upper()
    )
    types: Purchace = Product.objects.filter(discipline__name=item.name)
    return types


@sync_to_async
def get_item(dis: int, type_name: Type) -> Product:
    print(dis, type_name)
    target: Product = get_object_or_404(
        Product,
        discipline=dis,
        type=type_name.id
    )
    return target
    # types = Product.objects.filter(discipline__name=item.name)


@sync_to_async
def check_price(
        name: str,
        type_name: str
) -> decimal:
    dis: Discipline = get_object_or_404(
        Discipline,
        name=name
    )
    name_type: Type = get_object_or_404(
        Type,
        name=type_name
    )
    product: Product = Product.objects.get(
        discipline=dis.id,
        type=name_type.id
    )
    return product.price


@sync_to_async
def packing(person: int, cart: list[Product]) -> decimal:
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    user: Student = get_object_or_404(
        Student,
        id_user=person
    )
    obj: Purchace = Purchace.objects.create(
        buyer_id=user.id
    )
    print(f"{cart=}\n{user=}\t{obj=}\n{user.id=}\t{obj.id=}")
    for item in cart:
        print(item)
        ProductPurchase.objects.create(
            purchase=obj,
            product=item
        )
        print("-----------------------------------")
        obj.amount += item.price
        obj.save()
    return obj.amount
