# Generated by Django 3.1.6 on 2021-09-24 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0050_dostavlen_us'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='prdead',
            field=models.IntegerField(default=0),
        ),
    ]
