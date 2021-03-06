# Generated by Django 3.1.6 on 2021-07-18 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0015_auto_20210707_1450'),
    ]

    operations = [
        migrations.CreateModel(
            name='atributes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazv', models.CharField(default='NONE', max_length=150)),
                ('valtype', models.IntegerField()),
                ('groupid', models.IntegerField()),
                ('antogon', models.CharField(default='0', max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='before',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('val_int', models.IntegerField()),
                ('val_float', models.FloatField()),
                ('val_text', models.CharField(default='NONE', max_length=150)),
                ('groupid', models.IntegerField()),
                ('atrib', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hospital.atributes')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hospital.case')),
            ],
        ),
        migrations.CreateModel(
            name='after',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('val_int', models.IntegerField()),
                ('val_float', models.FloatField()),
                ('val_text', models.CharField(default='NONE', max_length=150)),
                ('groupid', models.IntegerField()),
                ('atrib', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hospital.atributes')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hospital.case')),
            ],
        ),
    ]
