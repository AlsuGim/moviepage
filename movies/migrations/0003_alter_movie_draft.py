# Generated by Django 4.0.4 on 2022-04-25 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_alter_rating_movie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='draft',
            field=models.BooleanField(default=False, verbose_name='Черновик'),
        ),
    ]
