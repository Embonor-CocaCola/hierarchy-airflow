# Generated by Django 3.2.9 on 2022-02-07 17:44

import datetime
from django.db import migrations, models
import django.db.models.deletion
import expos.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('etl_job', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BranchOfficeConform',
            fields=[
                ('source_id', models.IntegerField()),
                ('name', models.TextField()),
                ('plant_id', models.IntegerField()),
                ('created_at', expos.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('updated_at', expos.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('id', expos.models.AutoUUIDField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'airflow"."branch_office_conform',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='BranchOfficeRaw',
            fields=[
                ('source_id', models.TextField(blank=True, null=True)),
                ('name', models.TextField(blank=True, null=True)),
                ('plant_id', models.TextField(blank=True, null=True)),
                ('created_at', expos.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('updated_at', expos.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('id', expos.models.AutoUUIDField(editable=False, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'airflow"."branch_office_raw',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='BranchOfficeTyped',
            fields=[
                ('source_id', models.IntegerField()),
                ('name', models.TextField()),
                ('plant_id', models.IntegerField()),
                ('created_at', expos.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('updated_at', expos.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('id', expos.models.AutoUUIDField(primary_key=True, serialize=False)),
                ('job_id', models.ForeignKey(db_column='job_id', on_delete=django.db.models.deletion.CASCADE, to='etl_job.etljob')),
            ],
            options={
                'db_table': 'airflow"."branch_office_typed',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='BranchOfficeStaged',
            fields=[
                ('source_id', models.IntegerField()),
                ('name', models.TextField()),
                ('created_at', expos.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('updated_at', expos.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('id', expos.models.AutoUUIDField(primary_key=True, serialize=False)),
                ('job_id', models.ForeignKey(db_column='job_id', on_delete=django.db.models.deletion.CASCADE, to='etl_job.etljob')),
            ],
            options={
                'db_table': 'airflow"."branch_office_staged',
                'managed': True,
            },
        ),
    ]
