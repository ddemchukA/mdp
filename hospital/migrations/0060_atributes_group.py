# Generated by Django 3.1.6 on 2021-12-19 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0059_auto_20211128_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='atributes',
            name='group',
            field=models.IntegerField(default=0),
        ),
    ]
