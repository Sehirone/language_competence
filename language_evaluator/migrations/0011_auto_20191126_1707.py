# Generated by Django 2.2.4 on 2019-11-26 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('language_evaluator', '0010_auto_20191126_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='result',
            field=models.IntegerField(default=0),
        ),
    ]
