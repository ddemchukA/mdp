# Generated by Django 3.1.6 on 2021-08-13 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0029_auto_20210811_2154'),
    ]

    operations = [
        migrations.AddField(
            model_name='atributes',
            name='potomki',
            field=models.CharField(default='0', max_length=150),
        ),
    ]