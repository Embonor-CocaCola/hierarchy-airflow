from django.db import models
from gac.models import DateTimeWithoutTZField, AutoUUIDField
from datetime import datetime
from etl_job.models import EtlJob


class SurveyRaw(models.Model):
    source_id = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    paused = models.TextField(blank=True, null=True)
    portals = models.TextField(blank=True, null=True)
    valid_since = models.TextField(blank=True, null=True)
    valid_until = models.TextField(blank=True, null=True)
    external_created_at = models.TextField(blank=True, null=True)
    external_updated_at = models.TextField(blank=True, null=True)

    job_id = models.ForeignKey(
        EtlJob,
        on_delete=models.CASCADE,
        db_column='job_id',
    )

    created_at = DateTimeWithoutTZField(default=datetime.now)
    updated_at = DateTimeWithoutTZField(default=datetime.now)

    id = AutoUUIDField(primary_key=True, editable=False)

    class Meta:
        managed = True
        db_table = 'airflow\".\"survey_raw'


class SurveyTyped(models.Model):
    source_id = models.TextField()
    name = models.TextField()
    paused = models.BooleanField()
    portals = models.JSONField()
    valid_since = DateTimeWithoutTZField(null=True)
    valid_until = DateTimeWithoutTZField(null=True)
    external_created_at = DateTimeWithoutTZField()
    external_updated_at = DateTimeWithoutTZField()

    job_id = models.ForeignKey(
        EtlJob,
        on_delete=models.CASCADE,
        db_column='job_id',
    )

    created_at = DateTimeWithoutTZField(default=datetime.now)
    updated_at = DateTimeWithoutTZField(default=datetime.now)

    id = AutoUUIDField(primary_key=True, editable=False)

    class Meta:
        managed = True
        db_table = 'airflow\".\"survey_typed'
