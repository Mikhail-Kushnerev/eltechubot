# Generated by Django 4.0.6 on 2022-07-12 23:19

from django.db import migrations, models
import django.db.models.deletion
import django_project.telegrambot.unitems.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Наименование дисциплины')),
                ('lektor', models.CharField(blank=True, max_length=200, null=True, verbose_name='ФИО преподавателя')),
            ],
            options={
                'verbose_name': 'Дисциплина',
                'verbose_name_plural': 'Дисциплины',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=django_project.telegrambot.unitems.models.user_directory_path)),
                ('discipline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='unitems.discipline', verbose_name='дисциплина')),
            ],
            options={
                'verbose_name': 'Файл',
                'verbose_name_plural': 'Файлы',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Индивидуальное домашнее задание', 'ИДЗ'), ('Лабораторная работа', 'Л/Р'), ('Курсовая работа', 'КР'), ('Контрольная работа', 'К/Р')], max_length=150, unique=True, verbose_name='тип товара')),
            ],
            options={
                'verbose_name': 'вид деятельности',
                'verbose_name_plural': 'виды деятельности',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Purchace',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID покупки')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Стоимость')),
                ('purchase_time', models.DateTimeField(auto_now_add=True, verbose_name='Время покупки')),
                ('successful', models.BooleanField(default=False, verbose_name='Состояние покупки')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchaces', to='students.student')),
                ('item', models.ManyToManyField(related_name='purchaces', to='unitems.product')),
            ],
            options={
                'verbose_name': 'Покупка',
                'verbose_name_plural': 'Покупки',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='unitems.type', verbose_name='вид работы'),
        ),
    ]
