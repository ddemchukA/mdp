# Generated by Django 3.1.6 on 2021-08-08 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0025_auto_20210808_1211'),
    ]

    operations = [
        migrations.AddField(
            model_name='atributes',
            name='potomok',
            field=models.IntegerField(default=0),
        ),
    ]
