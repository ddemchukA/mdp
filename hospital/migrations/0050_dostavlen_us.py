# Generated by Django 3.1.6 on 2021-09-21 10:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hospital', '0049_dostavlen_lpu'),
    ]

    operations = [
        migrations.AddField(
            model_name='dostavlen',
            name='us',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
