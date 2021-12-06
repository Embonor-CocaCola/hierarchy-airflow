from django.db import models
from django.contrib.postgres.fields import ArrayField
from gac.models import DateTimeWithoutTZField, AutoUUIDField
from datetime import datetime
from etl_job.models import EtlJob


class AnswerRaw(models.Model):
    source_id = models.TextField(blank=True, null=True)
    survey_id = models.TextField(blank=True, null=True)
    latitude = models.TextField(blank=True, null=True)
    longitude = models.TextField(blank=True, null=True)
    skips_survey = models.TextField(blank=True, null=True)
    pollster_id = models.TextField(blank=True, null=True)
    surveyed_id = models.TextField(blank=True, null=True)
    external_created_at = models.TextField(blank=True, null=True)
    answers = models.TextField(blank=True, null=True)

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
        db_table = 'airflow\".\"answer_raw'


class AnswerTyped(models.Model):
    source_id = models.TextField()
    survey_id = models.TextField()
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    skips_survey = models.BooleanField()
    pollster_id = models.IntegerField()
    surveyed_id = models.IntegerField()
    external_created_at = DateTimeWithoutTZField()
    answers = models.JSONField()

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
        db_table = 'airflow\".\"answer_typed'


class SelfEvaluationConform(models.Model):
    source_id = models.TextField()
    skips_survey = models.BooleanField()
    vendor_id = models.IntegerField()
    customer_id = models.IntegerField()
    external_created_at = DateTimeWithoutTZField()

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
        db_table = 'airflow\".\"self_evaluation_conform'


class AnswerConform(models.Model):
    source_id = models.TextField()
    values = models.JSONField()
    attachments = ArrayField(models.TextField())
    observations = models.TextField(null=True)
    self_evaluation_id = models.UUIDField()
    question_id = models.TextField()

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
        db_table = 'airflow\".\"answer_conform'
