# Generated by Django 3.1.6 on 2021-09-20 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0046_delete_tolpu'),
    ]

    operations = [
        migrations.AddField(
            model_name='after',
            name='valtype',
            field=models.IntegerField(default=0),
        ),
    ]
