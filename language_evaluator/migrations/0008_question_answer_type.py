# Generated by Django 2.2.2 on 2019-11-23 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('language_evaluator', '0007_auto_20190621_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='answer_type',
            field=models.IntegerField(choices=[(0, 'Single'), (1, 'Multiple'), (2, 'True/False'), (3, 'Written'), (4, 'Spoken')], default=0),
        ),
    ]