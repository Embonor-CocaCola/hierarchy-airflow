# Generated by Django 3.2.9 on 2022-01-25 16:44

import datetime
from django.db import migrations, models
import django.db.models.deletion
import expos.models


class Migration(migrations.Migration):

    dependencies = [
        ('etl_job', '0004_create_find_question_id_from_portals_procedure'),
        ('answer', '0003_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SelfEvaluationFailedInserts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_id', models.TextField()),
                ('vendor_source_id', models.TextField()),
                ('customer_source_id', models.TextField()),
                ('vendor_name', models.TextField()),
                ('customer_name', models.TextField()),
                ('vendor_rut', models.TextField()),
                ('customer_rut', models.TextField()),
                ('created_at', expos.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('updated_at', expos.models.DateTimeWithoutTZField(default=datetime.datetime.now)),
                ('job_id', models.ForeignKey(db_column='job_id', on_delete=django.db.models.deletion.CASCADE, to='etl_job.etljob')),
            ],
            options={
                'db_table': 'airflow"."self_evaluation_failed',
                'managed': True,
            },
        ),
    ]