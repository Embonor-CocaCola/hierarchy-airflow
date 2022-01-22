# Generated by Django 3.2.9 on 2021-12-14 16:13

import datetime
from django.db import migrations, models
import django.db.models.deletion
import expos.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('plant', '0001_initial'),
        ('etl_job', '0004_create_find_question_id_from_portals_procedure'),
        ('supervisor_plant', '0001_initial'),
        ('branch_office', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorTyped',
            fields=[
                ('source_id', models.IntegerField()),
                ('name', models.TextField()),
                ('rut', models.TextField(blank=True, null=True)),
                ('email', models.TextField(blank=True, null=True)),
                ('phone', models.TextField(blank=True, null=True)),
                ('branch_office', models.IntegerField()),
                ('vendor_type_id', models.IntegerField()),
                ('operation_range', models.TextField(blank=True, null=True)),
                ('deleted_at', models.DateField(null=True)),
                ('driver_helper_code', models.TextField(blank=True, null=True)),
                ('created_at', expos.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('updated_at', expos.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('id', expos.models.AutoUUIDField(editable=False, primary_key=True, serialize=False)),
                ('job_id', models.ForeignKey(db_column='job_id', on_delete=django.db.models.deletion.CASCADE, to='etl_job.etljob')),
            ],
            options={
                'db_table': 'airflow"."vendor_typed',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='VendorStaged',
            fields=[
                ('source_id', models.IntegerField()),
                ('name', models.TextField()),
                ('rut', models.TextField(blank=True, null=True)),
                ('email', models.TextField(blank=True, null=True)),
                ('phone', models.TextField(blank=True, null=True)),
                ('vendor_type', models.TextField()),
                ('deleted_at', models.DateField(null=True)),
                ('created_at', expos.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('updated_at', expos.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('id', expos.models.AutoUUIDField(editable=False, primary_key=True, serialize=False)),
                ('branch_office_id', models.ForeignKey(db_column='branch_office_id', db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='branch_office.branchofficestaged')),
                ('job_id', models.ForeignKey(db_column='job_id', on_delete=django.db.models.deletion.CASCADE, to='etl_job.etljob')),
                ('plant_id', models.ForeignKey(db_column='plant_id', db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='plant.plantstaged')),
                ('supervisor_id', models.ForeignKey(db_column='supervisor_id', db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='supervisor_plant.supervisorstaged')),
            ],
            options={
                'db_table': 'airflow"."vendor_staged',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='VendorRaw',
            fields=[
                ('source_id', models.TextField(blank=True, null=True)),
                ('name', models.TextField(blank=True, null=True)),
                ('rut', models.TextField(blank=True, null=True)),
                ('email', models.TextField(blank=True, null=True)),
                ('phone', models.TextField(blank=True, null=True)),
                ('branch_office', models.TextField(blank=True, null=True)),
                ('vendor_type_id', models.TextField(blank=True, null=True)),
                ('operation_range', models.TextField(blank=True, null=True)),
                ('deleted_at', models.TextField(blank=True, null=True)),
                ('driver_helper_code', models.TextField(blank=True, null=True)),
                ('created_at', expos.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('updated_at', expos.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('id', expos.models.AutoUUIDField(editable=False, primary_key=True, serialize=False)),
                ('job_id', models.ForeignKey(db_column='job_id', on_delete=django.db.models.deletion.CASCADE, to='etl_job.etljob')),
            ],
            options={
                'db_table': 'airflow"."vendor_raw',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='VendorConform',
            fields=[
                ('source_id', models.IntegerField()),
                ('name', models.TextField()),
                ('rut', models.TextField(blank=True, null=True)),
                ('email', models.TextField(blank=True, null=True)),
                ('phone', models.TextField(blank=True, null=True)),
                ('branch_office_id', models.IntegerField()),
                ('vendor_type_id', models.IntegerField()),
                ('deleted_at', models.DateField(null=True)),
                ('created_at', expos.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('updated_at', expos.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('id', expos.models.AutoUUIDField(editable=False, primary_key=True, serialize=False)),
                ('job_id', models.ForeignKey(db_column='job_id', on_delete=django.db.models.deletion.CASCADE, to='etl_job.etljob')),
            ],
            options={
                'db_table': 'airflow"."vendor_conform',
                'managed': True,
            },
        ),
    ]