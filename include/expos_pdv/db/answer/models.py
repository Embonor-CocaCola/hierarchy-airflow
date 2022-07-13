from django.db import models
from django.contrib.postgres.fields import ArrayField

from customer.models import CustomerStaged
from etl_job.models import ExposEtlJob
from expos.models import DateTimeWithoutTZField, AutoUUIDField
from datetime import datetime
from question.models import QuestionStaged
from vendor.models import VendorStaged


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
        ExposEtlJob,
        on_delete=models.CASCADE,
        db_column='job_id',
    )

    created_at = DateTimeWithoutTZField(default=datetime.now)
    updated_at = DateTimeWithoutTZField(default=datetime.now)

    id = AutoUUIDField(primary_key=True, editable=False)

    class Meta:
        app_label = 'answer'
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
        ExposEtlJob,
        on_delete=models.CASCADE,
        db_column='job_id',
    )

    created_at = DateTimeWithoutTZField(default=datetime.now)
    updated_at = DateTimeWithoutTZField(default=datetime.now)

    id = AutoUUIDField(primary_key=True, editable=False)

    class Meta:
        app_label = 'answer'
        managed = True
        db_table = 'airflow\".\"answer_typed'


class SurveyConform(models.Model):
    source_id = models.TextField()
    source_survey_id = models.TextField(null=True)
    skips_survey = models.BooleanField()
    vendor_id = models.IntegerField()
    customer_id = models.IntegerField()
    external_created_at = DateTimeWithoutTZField()

    job_id = models.ForeignKey(
        ExposEtlJob,
        on_delete=models.CASCADE,
        db_column='job_id',
    )

    created_at = DateTimeWithoutTZField(default=datetime.now)
    updated_at = DateTimeWithoutTZField(default=datetime.now)

    id = AutoUUIDField(primary_key=True, editable=False)

    class Meta:
        app_label = 'answer'
        managed = True
        db_table = 'survey_conform'


class SurveyStaged(models.Model):
    source_id = models.TextField()
    source_survey_id = models.TextField(null=True)
    skips_survey = models.BooleanField()
    vendor_id = models.ForeignKey(VendorStaged, on_delete=models.CASCADE, db_column='vendor_id', db_constraint=False)
    customer_id = models.ForeignKey(
        CustomerStaged,
        on_delete=models.CASCADE,
        db_column='customer_id',
        db_constraint=False,
    )
    external_created_at = DateTimeWithoutTZField()

    job_id = models.ForeignKey(
        ExposEtlJob,
        on_delete=models.CASCADE,
        db_column='job_id',
    )

    created_at = DateTimeWithoutTZField(default=datetime.now)
    updated_at = DateTimeWithoutTZField(default=datetime.now)

    id = AutoUUIDField(primary_key=True, editable=False)

    class Meta:
        app_label = 'answer'
        managed = True
        db_table = 'survey_staged'


class AnswerConform(models.Model):
    source_id = models.TextField()
    values = models.JSONField()
    attachments = ArrayField(models.TextField())
    observations = models.TextField(null=True)
    survey_id = models.UUIDField()
    question_id = models.TextField()

    job_id = models.ForeignKey(
        ExposEtlJob,
        on_delete=models.CASCADE,
        db_column='job_id',
    )

    created_at = DateTimeWithoutTZField(default=datetime.now)
    updated_at = DateTimeWithoutTZField(default=datetime.now)

    id = AutoUUIDField(primary_key=True, editable=False)

    class Meta:
        app_label = 'answer'
        managed = True
        db_table = 'airflow\".\"answer_conform'


class AnswerStaged(models.Model):
    source_id = models.TextField()
    values = models.JSONField()
    attachments = ArrayField(models.TextField())
    observations = models.TextField(null=True)
    survey_id = models.UUIDField()
    question_id = models.ForeignKey(
        QuestionStaged,
        on_delete=models.CASCADE,
        db_column='question_id',
        db_constraint=False,
    )

    job_id = models.ForeignKey(
        ExposEtlJob,
        on_delete=models.CASCADE,
        db_column='job_id',
    )

    created_at = DateTimeWithoutTZField(default=datetime.now)
    updated_at = DateTimeWithoutTZField(default=datetime.now)

    id = AutoUUIDField(primary_key=True, editable=False)

    class Meta:
        app_label = 'answer'
        managed = True
        db_table = 'airflow\".\"answer_staged'


class SurveyFailedInserts(models.Model):
    source_id = models.TextField()

    vendor_source_id = models.TextField(null=True)
    customer_source_id = models.TextField(null=True)
    vendor_name = models.TextField(null=True)
    customer_name = models.TextField(null=True)

    job_id = models.ForeignKey(
        ExposEtlJob,
        on_delete=models.CASCADE,
        db_column='job_id',
    )

    created_at = DateTimeWithoutTZField(default=datetime.now)
    updated_at = DateTimeWithoutTZField(default=datetime.now)

    class Meta:
        app_label = 'answer'
        managed = True
        db_table = 'airflow\".\"survey_failed'
