from django.db import models
from gac.models import DateTimeWithoutTZField, AutoUUIDField
from datetime import datetime
from etl_job.models import EtlJob


class VendorRaw(models.Model):
    source_id = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    rut = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    branch_office = models.TextField(blank=True, null=True)
    vendor_type_id = models.TextField(blank=True, null=True)
    operation_range = models.TextField(blank=True, null=True)
    deleted_at = models.TextField(blank=True, null=True)
    driver_helper_code = models.TextField(blank=True, null=True)

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
        db_table = 'airflow\".\"vendor_raw'


class VendorTyped(models.Model):
    source_id = models.IntegerField()
    name = models.TextField()
    rut = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    branch_office = models.IntegerField()
    vendor_type_id = models.IntegerField()
    operation_range = models.TextField(blank=True, null=True)
    deleted_at = models.DateField(null=True)
    driver_helper_code = models.TextField(blank=True, null=True)

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
        db_table = 'airflow\".\"vendor_typed'


class VendorConform(models.Model):
    source_id = models.IntegerField()
    name = models.TextField()
    rut = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    branch_office_id = models.IntegerField()
    vendor_type_id = models.IntegerField()
    deleted_at = models.DateField(null=True)

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
        db_table = 'airflow\".\"vendor_conform'
