# Generated by Django 3.1.6 on 2021-08-27 05:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0039_auto_20210827_1138'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='intime',
            name='case',
        ),
    ]
