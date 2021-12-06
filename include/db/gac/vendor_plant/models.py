from django.db import models
from gac.models import DateTimeWithoutTZField, AutoUUIDField
from datetime import datetime
from etl_job.models import EtlJob


class VendorPlantRaw(models.Model):
    vendor_id = models.TextField(blank=True, null=True)
    supervisor_id = models.TextField(blank=True, null=True)
    chief_rut = models.TextField(blank=True, null=True)
    plant_id = models.TextField(blank=True, null=True)

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
        db_table = 'airflow\".\"vendor_plant_raw'


class VendorPlantTyped(models.Model):
    vendor_id = models.IntegerField()
    supervisor_id = models.IntegerField()
    chief_rut = models.TextField()
    plant_id = models.IntegerField()

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
        db_table = 'airflow\".\"vendor_plant_typed'


class VendorPlantConform(models.Model):
    vendor_id = models.IntegerField()
    supervisor_id = models.UUIDField()
    plant_id = models.UUIDField()

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
        db_table = 'airflow\".\"vendor_plant_conform'
