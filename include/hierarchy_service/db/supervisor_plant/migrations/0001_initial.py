# Generated by Django 3.2.9 on 2022-07-20 20:28

import datetime
from django.db import migrations, models
import django.db.models.deletion
import hierarchy.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('etl_job', '0001_initial'),
        ('chief_plant', '0002_initial'),
        ('plant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupervisorStaged',
            fields=[
                ('source_id', models.IntegerField()),
                ('code', models.TextField(blank=True, null=True)),
                ('name', models.TextField()),
                ('location', models.TextField(blank=True, null=True)),
                ('role', models.TextField(blank=True, null=True)),
                ('created_at', hierarchy.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('updated_at', hierarchy.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('id', hierarchy.models.AutoUUIDField(editable=False, primary_key=True, serialize=False)),
                ('chief_id', models.ForeignKey(db_column='chief_id', db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='chief_plant.chiefstaged')),
                ('job_id', models.ForeignKey(db_column='job_id', on_delete=django.db.models.deletion.CASCADE, to='etl_job.etljob')),
                ('plant_id', models.ForeignKey(db_column='plant_id', db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='plant.plantstaged')),
            ],
            options={
                'db_table': 'airflow"."supervisor_staged',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SupervisorPlantTyped',
            fields=[
                ('supervisor_id', models.IntegerField()),
                ('supervisor_code', models.TextField(blank=True, null=True)),
                ('supervisor_name', models.TextField()),
                ('supervisor_location', models.TextField(blank=True, null=True)),
                ('chief_id', models.IntegerField()),
                ('plant_id', models.IntegerField()),
                ('role', models.TextField(blank=True, null=True)),
                ('chief_unit', models.TextField(blank=True, null=True)),
                ('created_at', hierarchy.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('updated_at', hierarchy.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('id', hierarchy.models.AutoUUIDField(editable=False, primary_key=True, serialize=False)),
                ('job_id', models.ForeignKey(db_column='job_id', on_delete=django.db.models.deletion.CASCADE, to='etl_job.etljob')),
            ],
            options={
                'db_table': 'airflow"."supervisor_plant_typed',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SupervisorPlantRaw',
            fields=[
                ('supervisor_id', models.TextField(blank=True, null=True)),
                ('supervisor_code', models.TextField(blank=True, null=True)),
                ('supervisor_name', models.TextField(blank=True, null=True)),
                ('supervisor_location', models.TextField(blank=True, null=True)),
                ('chief_id', models.TextField(blank=True, null=True)),
                ('plant_id', models.TextField(blank=True, null=True)),
                ('role', models.TextField(blank=True, null=True)),
                ('chief_unit', models.TextField(blank=True, null=True)),
                ('created_at', hierarchy.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('updated_at', hierarchy.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('id', hierarchy.models.AutoUUIDField(editable=False, primary_key=True, serialize=False)),
                ('job_id', models.ForeignKey(db_column='job_id', on_delete=django.db.models.deletion.CASCADE, to='etl_job.etljob')),
            ],
            options={
                'db_table': 'airflow"."supervisor_plant_raw',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SupervisorConform',
            fields=[
                ('source_id', models.IntegerField()),
                ('code', models.TextField(blank=True, null=True)),
                ('name', models.TextField()),
                ('location', models.TextField(blank=True, null=True)),
                ('chief_id', models.IntegerField()),
                ('plant_id', models.IntegerField()),
                ('role', models.TextField(blank=True, null=True)),
                ('created_at', hierarchy.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('updated_at', hierarchy.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('id', hierarchy.models.AutoUUIDField(editable=False, primary_key=True, serialize=False)),
                ('job_id', models.ForeignKey(db_column='job_id', on_delete=django.db.models.deletion.CASCADE, to='etl_job.etljob')),
            ],
            options={
                'db_table': 'airflow"."supervisor_conform',
                'managed': True,
            },
        ),
    ]
