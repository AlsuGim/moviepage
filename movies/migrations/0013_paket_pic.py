# Generated by Django 4.0.4 on 2022-05-20 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0012_alter_paket_months_alter_paket_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='paket',
            name='pic',
            field=models.ImageField(blank=True, null=True, upload_to='images/pakets', verbose_name='Изображение'),
        ),
    ]
