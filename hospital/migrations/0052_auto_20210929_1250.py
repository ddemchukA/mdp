# Generated by Django 3.1.6 on 2021-09-29 05:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0051_patient_prdead'),
    ]

    operations = [
        migrations.CreateModel(
            name='sex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sex', models.CharField(default='M', max_length=1)),
            ],
        ),
        migrations.AddField(
            model_name='patient',
            name='pol',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hospital.sex'),
        ),
    ]
