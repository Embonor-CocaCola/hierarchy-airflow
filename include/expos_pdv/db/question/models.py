from django.db import models
from include.expos_pdv.db.expos.models import DateTimeWithoutTZField, AutoUUIDField
from datetime import datetime
from include.expos_pdv import EtlJob


class QuestionRaw(models.Model):
    source_id = models.TextField(blank=True, null=True)
    attach = models.TextField(blank=True, null=True)
    heading = models.TextField(blank=True, null=True)
    options = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    sub_type = models.TextField(blank=True, null=True)
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
        db_table = 'airflow\".\"question_raw'


class QuestionTyped(models.Model):
    source_id = models.TextField()
    attach = models.JSONField()
    heading = models.TextField()
    options = models.JSONField()
    type = models.TextField()
    sub_type = models.TextField()
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
        db_table = 'airflow\".\"question_typed'


class QuestionConform(models.Model):
    source_id = models.TextField()
    attach = models.JSONField()
    heading = models.TextField()
    options = models.JSONField()
    type = models.TextField()
    sub_type = models.TextField()
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
        db_table = 'airflow\".\"question_conform'


class QuestionStaged(models.Model):
    source_id = models.TextField()
    heading = models.TextField()
    options = models.JSONField()
    type = models.TextField()
    sub_type = models.TextField()
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
        db_table = 'airflow\".\"question_staged'
