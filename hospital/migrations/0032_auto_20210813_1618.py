# Generated by Django 3.1.6 on 2021-08-13 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0031_atributes_umolch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atributes',
            name='umolch',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
    ]
