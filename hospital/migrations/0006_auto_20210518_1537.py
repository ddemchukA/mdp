# Generated by Django 3.1.6 on 2021-05-18 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0005_insultik_rezult'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insultik',
            name='rezult',
            field=models.IntegerField(),
        ),
    ]