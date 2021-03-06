# Generated by Django 3.1.3 on 2021-06-02 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interviewer', '0014_interviewdata_marks_in_perc'),
    ]

    operations = [
        migrations.AddField(
            model_name='interviewdata',
            name='accuracy_eighty_words',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='interviewdata',
            name='accuracy_hundred_words',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='interviewdata',
            name='accuracy_zero_words',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
