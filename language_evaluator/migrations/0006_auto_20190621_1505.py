# Generated by Django 2.2.2 on 2019-06-21 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('language_evaluator', '0005_test_current_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.CharField(max_length=200),
        ),
    ]
