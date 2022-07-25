from django.db import models

from etl_job.models import EtlJob
from hierarchy.models import DateTimeWithoutTZField, AutoUUIDField
from datetime import datetime


class VendorPlantRaw(models.Model):
    vendor_id = models.TextField(blank=True, null=True)
    supervisor_id = models.TextField(blank=True, null=True)
    chief_rut = models.TextField(blank=True, null=True)
    plant_id = models.TextField(blank=True, null=True)
    vendor_name = models.TextField(blank=True, null=True)

    job_id = models.ForeignKey(
        EtlJob,
        on_delete=models.CASCADE,
        db_column='job_id',
    )

    created_at = DateTimeWithoutTZField(default=datetime.now)
    updated_at = DateTimeWithoutTZField(default=datetime.now)

    id = AutoUUIDField(primary_key=True, editable=False)

    class Meta:
        app_label = 'vendor_plant'
        managed = True
        db_table = 'airflow\".\"vendor_plant_raw'


class VendorPlantTyped(models.Model):
    vendor_id = models.IntegerField()
    supervisor_id = models.IntegerField()
    chief_rut = models.TextField()
    plant_id = models.IntegerField()
    vendor_name = models.TextField(blank=True, null=True)

    job_id = models.ForeignKey(
        EtlJob,
        on_delete=models.CASCADE,
        db_column='job_id',
    )

    created_at = DateTimeWithoutTZField(default=datetime.now)
    updated_at = DateTimeWithoutTZField(default=datetime.now)

    id = AutoUUIDField(primary_key=True, editable=False)

    class Meta:
        app_label = 'vendor_plant'
        managed = True
        db_table = 'airflow\".\"vendor_plant_typed'


class VendorPlantConform(models.Model):
    vendor_id = models.IntegerField()
    supervisor_id = models.UUIDField()
    plant_id = models.UUIDField()
    vendor_name = models.TextField(blank=True, null=True)

    job_id = models.ForeignKey(
        EtlJob,
        on_delete=models.CASCADE,
        db_column='job_id',
    )

    created_at = DateTimeWithoutTZField(default=datetime.now)
    updated_at = DateTimeWithoutTZField(default=datetime.now)

    id = AutoUUIDField(primary_key=True, editable=False)

    class Meta:
        app_label = 'vendor_plant'
        managed = True
        db_table = 'airflow\".\"vendor_plant_conform'
