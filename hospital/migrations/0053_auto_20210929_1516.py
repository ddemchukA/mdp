# Generated by Django 3.1.6 on 2021-09-29 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0052_auto_20210929_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='vputi',
            field=models.IntegerField(default=-1),
        ),
    ]
