# Generated by Django 4.0.4 on 2022-05-22 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0013_paket_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default='static/images/user.png', null=False, blank=False, upload_to='images/users', verbose_name='Изображение'),
        ),
    ]