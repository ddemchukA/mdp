# Generated by Django 3.1.6 on 2021-08-08 05:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0023_case_fromlpu'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='before',
            name='val_int',
        ),
    ]
