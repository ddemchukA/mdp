# Generated by Django 3.1.6 on 2021-03-09 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0002_auto_kadri_pribor'),
    ]

    operations = [
        migrations.CreateModel(
            name='spr_dinam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nazv', models.CharField(max_length=50)),
                ('pr_evac', models.BooleanField(default=False)),
                ('pr_zak', models.BooleanField(default=False)),
            ],
        ),
    ]
