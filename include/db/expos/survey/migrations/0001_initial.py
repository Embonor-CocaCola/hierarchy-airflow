# Generated by Django 3.2.9 on 2021-12-14 16:13

import datetime
from django.db import migrations, models
import django.db.models.deletion
import expos.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('etl_job', '0004_create_find_question_id_from_portals_procedure'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurveyTyped',
            fields=[
                ('source_id', models.TextField()),
                ('name', models.TextField()),
                ('paused', models.BooleanField()),
                ('portals', models.JSONField()),
                ('valid_since', expos.models.DateTimeWithoutTZField(null=True)),
                ('valid_until', expos.models.DateTimeWithoutTZField(null=True)),
                ('external_created_at', expos.models.DateTimeWithoutTZField()),
                ('external_updated_at', expos.models.DateTimeWithoutTZField()),
                ('created_at', expos.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('updated_at', expos.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('id', expos.models.AutoUUIDField(editable=False, primary_key=True, serialize=False)),
                ('job_id', models.ForeignKey(db_column='job_id', on_delete=django.db.models.deletion.CASCADE, to='etl_job.etljob')),
            ],
            options={
                'db_table': 'airflow"."survey_typed',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SurveyRaw',
            fields=[
                ('source_id', models.TextField(blank=True, null=True)),
                ('name', models.TextField(blank=True, null=True)),
                ('paused', models.TextField(blank=True, null=True)),
                ('portals', models.TextField(blank=True, null=True)),
                ('valid_since', models.TextField(blank=True, null=True)),
                ('valid_until', models.TextField(blank=True, null=True)),
                ('external_created_at', models.TextField(blank=True, null=True)),
                ('external_updated_at', models.TextField(blank=True, null=True)),
                ('created_at', expos.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('updated_at', expos.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('id', expos.models.AutoUUIDField(editable=False, primary_key=True, serialize=False)),
                ('job_id', models.ForeignKey(db_column='job_id', on_delete=django.db.models.deletion.CASCADE, to='etl_job.etljob')),
            ],
            options={
                'db_table': 'airflow"."survey_raw',
                'managed': True,
            },
        ),
    ]