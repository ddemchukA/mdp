# Generated by Django 3.1.6 on 2021-11-28 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0057_profile_is_superman'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fromlpu',
            name='roadrate',
            field=models.FloatField(default=0),
        ),
    ]