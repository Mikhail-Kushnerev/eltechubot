# Generated by Django 4.0.6 on 2022-07-30 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='username',
            field=models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='Nickname пользователя'),
        ),
    ]