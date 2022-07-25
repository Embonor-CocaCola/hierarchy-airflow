from django.db import models

from etl_job.models import EtlJob
from hierarchy.models import DateTimeWithoutTZField, AutoUUIDField
from datetime import datetime


class ClusterConform(models.Model):
    name = models.TextField()

    job_id = models.ForeignKey(
        EtlJob,
        on_delete=models.CASCADE,
        db_column='job_id',
    )

    created_at = DateTimeWithoutTZField(default=datetime.now)
    updated_at = DateTimeWithoutTZField(default=datetime.now)

    id = AutoUUIDField(primary_key=True, editable=False)

    class Meta:
        app_label = 'cluster'
        managed = True
        db_table = 'airflow\".\"cluster_conform'


class ClusterStaged(models.Model):
    name = models.TextField()

    job_id = models.ForeignKey(
        EtlJob,
        on_delete=models.CASCADE,
        db_column='job_id',
    )

    created_at = DateTimeWithoutTZField(default=datetime.now)
    updated_at = DateTimeWithoutTZField(default=datetime.now)

    id = models.UUIDField(primary_key=True, editable=False)

    class Meta:
        app_label = 'cluster'
        managed = True
        db_table = 'airflow\".\"cluster_staged'
