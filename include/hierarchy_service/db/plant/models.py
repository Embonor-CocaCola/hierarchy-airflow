from django.db import models

from etl_job.models import EtlJob
from hierarchy.models import DateTimeWithoutTZField, AutoUUIDField
from datetime import datetime


class PlantRaw(models.Model):
    source_id = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    job_id = models.ForeignKey(
        EtlJob,
        on_delete=models.CASCADE,
        db_column='job_id',
    )
    created_at = DateTimeWithoutTZField(default=datetime.now)
    updated_at = DateTimeWithoutTZField(default=datetime.now)

    id = AutoUUIDField(primary_key=True, editable=False)

    class Meta:
        app_label = 'plant'
        managed = True
        db_table = 'airflow\".\"plant_raw'


class PlantTyped(models.Model):
    source_id = models.IntegerField()
    name = models.TextField()

    job_id = models.ForeignKey(
        EtlJob,
        on_delete=models.CASCADE,
        db_column='job_id',
    )

    created_at = DateTimeWithoutTZField(default=datetime.now)
    updated_at = DateTimeWithoutTZField(default=datetime.now)

    id = models.UUIDField(primary_key=True)

    class Meta:
        app_label = 'plant'
        managed = True
        db_table = 'airflow\".\"plant_typed'


class PlantConform(models.Model):
    source_id = models.IntegerField()
    name = models.TextField()

    job_id = models.ForeignKey(
        EtlJob,
        on_delete=models.CASCADE,
        db_column='job_id',
    )

    created_at = DateTimeWithoutTZField(default=datetime.now)
    updated_at = DateTimeWithoutTZField(default=datetime.now)

    id = models.UUIDField(primary_key=True)

    class Meta:
        app_label = 'plant'
        managed = True
        db_table = 'airflow\".\"plant_conform'


class PlantStaged(models.Model):
    source_id = models.IntegerField()
    name = models.TextField()

    job_id = models.ForeignKey(
        EtlJob,
        on_delete=models.CASCADE,
        db_column='job_id',
    )

    created_at = DateTimeWithoutTZField(default=datetime.now)
    updated_at = DateTimeWithoutTZField(default=datetime.now)

    id = models.UUIDField(primary_key=True)

    class Meta:
        app_label = 'plant'
        managed = True
        db_table = 'airflow\".\"plant_staged'
