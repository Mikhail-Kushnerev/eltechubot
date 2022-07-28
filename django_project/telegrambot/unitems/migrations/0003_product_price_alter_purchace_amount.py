# Generated by Django 4.0.6 on 2022-07-28 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unitems', '0002_alter_type_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, default=50, max_digits=5, verbose_name='Стоимость'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='purchace',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, verbose_name='Стоимость'),
        ),
    ]
