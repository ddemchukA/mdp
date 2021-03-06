# Generated by Django 3.1.6 on 2021-07-06 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0013_patient'),
    ]

    operations = [
        migrations.CreateModel(
            name='doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fio', models.CharField(default='NONE', max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='fromlpu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazv', models.CharField(default='NONE', max_length=150)),
                ('roadrate', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='srmp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fio', models.CharField(default='NONE', max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='transport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazv', models.CharField(default='NONE', max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='case',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateti', models.DateTimeField(default='datetime.now')),
                ('dslpu', models.CharField(default='NONE', max_length=150)),
                ('dscons', models.CharField(default='NONE', max_length=150)),
                ('vzyat', models.DateTimeField(default='datetime.now')),
                ('id_doct', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hospital.transport')),
                ('id_pac', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hospital.patient')),
                ('id_trans', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hospital.doctor')),
            ],
        ),
    ]
