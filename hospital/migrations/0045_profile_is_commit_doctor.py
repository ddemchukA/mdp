# Generated by Django 3.1.6 on 2021-08-29 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0044_remove_case_todost'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_commit_doctor',
            field=models.BooleanField(default=False),
        ),
    ]
