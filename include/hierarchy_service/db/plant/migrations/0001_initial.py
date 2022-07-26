# Generated by Django 3.2.9 on 2022-07-20 20:28

import datetime
from django.db import migrations, models
import django.db.models.deletion
import hierarchy.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('etl_job', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlantTyped',
            fields=[
                ('source_id', models.IntegerField()),
                ('name', models.TextField()),
                ('created_at', hierarchy.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('updated_at', hierarchy.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('job_id', models.ForeignKey(db_column='job_id', on_delete=django.db.models.deletion.CASCADE, to='etl_job.etljob')),
            ],
            options={
                'db_table': 'airflow"."plant_typed',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PlantStaged',
            fields=[
                ('source_id', models.IntegerField()),
                ('name', models.TextField()),
                ('created_at', hierarchy.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('updated_at', hierarchy.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('job_id', models.ForeignKey(db_column='job_id', on_delete=django.db.models.deletion.CASCADE, to='etl_job.etljob')),
            ],
            options={
                'db_table': 'airflow"."plant_staged',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PlantRaw',
            fields=[
                ('source_id', models.TextField(blank=True, null=True)),
                ('name', models.TextField(blank=True, null=True)),
                ('created_at', hierarchy.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('updated_at', hierarchy.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('id', hierarchy.models.AutoUUIDField(editable=False, primary_key=True, serialize=False)),
                ('job_id', models.ForeignKey(db_column='job_id', on_delete=django.db.models.deletion.CASCADE, to='etl_job.etljob')),
            ],
            options={
                'db_table': 'airflow"."plant_raw',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PlantConform',
            fields=[
                ('source_id', models.IntegerField()),
                ('name', models.TextField()),
                ('created_at', hierarchy.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('updated_at', hierarchy.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('job_id', models.ForeignKey(db_column='job_id', on_delete=django.db.models.deletion.CASCADE, to='etl_job.etljob')),
            ],
            options={
                'db_table': 'airflow"."plant_conform',
                'managed': True,
            },
        ),
    ]
