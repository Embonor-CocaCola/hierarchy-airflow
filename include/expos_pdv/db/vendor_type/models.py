from django.db import models

from etl_job.models import ExposEtlJob
from expos.models import DateTimeWithoutTZField, AutoUUIDField
from datetime import datetime


class VendorTypeRaw(models.Model):
    source_id = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)

    job_id = models.ForeignKey(
        ExposEtlJob,
        on_delete=models.CASCADE,
        db_column='job_id',
    )

    created_at = DateTimeWithoutTZField(default=datetime.now)
    updated_at = DateTimeWithoutTZField(default=datetime.now)

    id = AutoUUIDField(primary_key=True, editable=False)

    class Meta:
        app_label = 'vendor_type'
        managed = True
        db_table = 'airflow\".\"vendor_type_raw'


class VendorTypeTyped(models.Model):
    source_id = models.IntegerField()
    name = models.TextField()

    job_id = models.ForeignKey(
        ExposEtlJob,
        on_delete=models.CASCADE,
        db_column='job_id',
    )

    created_at = DateTimeWithoutTZField(default=datetime.now)
    updated_at = DateTimeWithoutTZField(default=datetime.now)

    id = AutoUUIDField(primary_key=True, editable=False)

    class Meta:
        app_label = 'vendor_type'
        managed = True
        db_table = 'airflow\".\"vendor_type_typed'


class VendorTypeConform(models.Model):
    source_id = models.IntegerField()
    name = models.TextField()

    job_id = models.ForeignKey(
        ExposEtlJob,
        on_delete=models.CASCADE,
        db_column='job_id',
    )

    created_at = DateTimeWithoutTZField(default=datetime.now)
    updated_at = DateTimeWithoutTZField(default=datetime.now)

    id = AutoUUIDField(primary_key=True, editable=False)

    class Meta:
        app_label = 'vendor_type'
        managed = True
        db_table = 'airflow\".\"vendor_type_conform'
