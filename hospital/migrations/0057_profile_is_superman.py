# Generated by Django 3.1.6 on 2021-10-28 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0056_deadinroad_primech'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_superman',
            field=models.BooleanField(default=False),
        ),
    ]
