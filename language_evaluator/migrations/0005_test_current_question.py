# Generated by Django 2.2.2 on 2019-06-21 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('language_evaluator', '0004_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='current_question',
            field=models.IntegerField(default=0),
        ),
    ]