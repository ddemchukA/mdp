# Generated by Django 3.1.6 on 2021-09-30 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0055_remove_deadinroad_valtype'),
    ]

    operations = [
        migrations.AddField(
            model_name='deadinroad',
            name='primech',
            field=models.CharField(default='NONE', max_length=250),
        ),
    ]
