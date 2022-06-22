# Generated by Django 4.0.4 on 2022-05-16 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0010_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название пакета')),
                ('price', models.IntegerField(max_length=4, verbose_name='Цена пакета')),
                ('months', models.IntegerField(max_length=2, verbose_name='Количество месяцев')),
            ],
            options={
                'verbose_name': 'Пакет',
                'verbose_name_plural': 'Пакеты',
            },
        ),
    ]