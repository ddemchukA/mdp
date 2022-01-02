# Generated by Django 3.1.6 on 2021-09-30 13:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0053_auto_20210929_1516'),
    ]

    operations = [
        migrations.CreateModel(
            name='deadinroad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default='datetime.now')),
                ('valtype', models.IntegerField(default=0)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hospital.case')),
            ],
        ),
    ]
