# Generated by Django 3.1.6 on 2021-09-21 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0047_after_valtype'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dostavlen',
            old_name='timedost',
            new_name='timedeist',
        ),
        migrations.RemoveField(
            model_name='dostavlen',
            name='timepriem',
        ),
        migrations.AddField(
            model_name='dostavlen',
            name='whatis',
            field=models.IntegerField(default=0),
        ),
    ]
