# Generated by Django 3.1.3 on 2021-04-17 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interviewer', '0006_auto_20210415_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interviewdata',
            name='accuracy_eighty',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='interviewdata',
            name='accuracy_hundred',
            field=models.JSONField(null=True),
        ),
    ]