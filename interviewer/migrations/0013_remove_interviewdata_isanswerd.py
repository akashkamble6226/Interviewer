# Generated by Django 3.1.3 on 2021-05-31 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interviewer', '0012_interviewdata_isanswerd'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='interviewdata',
            name='isAnswerd',
        ),
    ]