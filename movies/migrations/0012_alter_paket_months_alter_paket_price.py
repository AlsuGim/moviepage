# Generated by Django 4.0.4 on 2022-05-17 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0011_paket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paket',
            name='months',
            field=models.IntegerField(verbose_name='Количество месяцев'),
        ),
        migrations.AlterField(
            model_name='paket',
            name='price',
            field=models.IntegerField( verbose_name='Цена пакета'),
        ),
    ]
