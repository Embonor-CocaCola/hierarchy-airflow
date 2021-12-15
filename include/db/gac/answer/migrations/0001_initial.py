# Generated by Django 3.2.9 on 2021-12-14 16:13

import datetime
import django.contrib.postgres.fields
from django.db import migrations, models
import gac.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerConform',
            fields=[
                ('source_id', models.TextField()),
                ('values', models.JSONField()),
                ('attachments', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=None)),
                ('observations', models.TextField(null=True)),
                ('self_evaluation_id', models.UUIDField()),
                ('question_id', models.TextField()),
                ('created_at', gac.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('updated_at', gac.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('id', gac.models.AutoUUIDField(editable=False, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'airflow"."answer_conform',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='AnswerRaw',
            fields=[
                ('source_id', models.TextField(blank=True, null=True)),
                ('survey_id', models.TextField(blank=True, null=True)),
                ('latitude', models.TextField(blank=True, null=True)),
                ('longitude', models.TextField(blank=True, null=True)),
                ('skips_survey', models.TextField(blank=True, null=True)),
                ('pollster_id', models.TextField(blank=True, null=True)),
                ('surveyed_id', models.TextField(blank=True, null=True)),
                ('external_created_at', models.TextField(blank=True, null=True)),
                ('answers', models.TextField(blank=True, null=True)),
                ('created_at', gac.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('updated_at', gac.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('id', gac.models.AutoUUIDField(editable=False, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'airflow"."answer_raw',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='AnswerStaged',
            fields=[
                ('source_id', models.TextField()),
                ('values', models.JSONField()),
                ('attachments', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=None)),
                ('observations', models.TextField(null=True)),
                ('self_evaluation_id', models.UUIDField()),
                ('created_at', gac.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('updated_at', gac.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('id', gac.models.AutoUUIDField(editable=False, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'airflow"."answer_staged',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='AnswerTyped',
            fields=[
                ('source_id', models.TextField()),
                ('survey_id', models.TextField()),
                ('latitude', models.FloatField(null=True)),
                ('longitude', models.FloatField(null=True)),
                ('skips_survey', models.BooleanField()),
                ('pollster_id', models.IntegerField()),
                ('surveyed_id', models.IntegerField()),
                ('external_created_at', gac.models.DateTimeWithoutTZField()),
                ('answers', models.JSONField()),
                ('created_at', gac.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('updated_at', gac.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('id', gac.models.AutoUUIDField(editable=False, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'airflow"."answer_typed',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SelfEvaluationConform',
            fields=[
                ('source_id', models.TextField()),
                ('skips_survey', models.BooleanField()),
                ('vendor_id', models.IntegerField()),
                ('customer_id', models.IntegerField()),
                ('external_created_at', gac.models.DateTimeWithoutTZField()),
                ('created_at', gac.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('updated_at', gac.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('id', gac.models.AutoUUIDField(editable=False, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'airflow"."self_evaluation_conform',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SelfEvaluationStaged',
            fields=[
                ('source_id', models.TextField()),
                ('skips_survey', models.BooleanField()),
                ('external_created_at', gac.models.DateTimeWithoutTZField()),
                ('created_at', gac.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('updated_at', gac.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('id', gac.models.AutoUUIDField(editable=False, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'airflow"."self_evaluation_staged',
                'managed': True,
            },
        ),
    ]
